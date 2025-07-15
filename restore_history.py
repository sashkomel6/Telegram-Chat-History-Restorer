import os
import asyncio
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import TelegramError
import re

# === CONFIGURATION ===
BOT1_TOKEN = "<BOT1_TOKEN>"  # 🔧 Replace with your first bot token
BOT2_TOKEN = "<BOT2_TOKEN>"  # 🔧 Replace with your second bot token
CHANNEL_ID = <CHANNEL_ID>    # 🔧 Replace with your target Telegram channel ID
MEDIA_PATH = "/path/to/your/exported/files"  # 🔧 Replace with your path
DELAY_SECONDS = 1.0

# Define author names exactly as they appear in your HTML export (lowercased, stripped)
AUTHOR_1 = "author_1_name"
AUTHOR_2 = "author_2_name"

bot1 = Bot(token=BOT1_TOKEN)
bot2 = Bot(token=BOT2_TOKEN)

async def safe_send(coro):
    while True:
        try:
            await coro
            break
        except TelegramError as e:
            msg = str(e)
            if 'Flood control exceeded' in msg:
                match = re.search(r"Retry in (\d+) seconds", msg)
                if match:
                    retry_after = int(match.group(1)) + 1
                    print(f"Flood control hit, waiting {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"Flood control hit, waiting 10 seconds fallback...")
                    await asyncio.sleep(10)
            elif 'Timed out' in msg:
                print("Telegram API timed out. Retrying in 5 seconds...")
                await asyncio.sleep(5)
                continue
            else:
                print(f"Telegram API error: {e}")
                break
        except Exception as e:
            print(f"Other error: {e}")
            break

async def post_text(bot, text):
    await safe_send(bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='HTML'))

async def post_media(bot, media_type, file_path, caption=None):
    try:
        with open(file_path, 'rb') as f:
            if media_type == 'photo':
                await safe_send(bot.send_photo(chat_id=CHANNEL_ID, photo=f, caption=caption))
            elif media_type == 'video':
                await safe_send(bot.send_video(chat_id=CHANNEL_ID, video=f, caption=caption))
            elif media_type == 'voice':
                await safe_send(bot.send_voice(chat_id=CHANNEL_ID, voice=f, caption=caption))
            elif media_type == 'document':
                await safe_send(bot.send_document(chat_id=CHANNEL_ID, document=f, caption=caption))
    except FileNotFoundError:
        print(f"File not found: {file_path}")

async def process_message(bot, text, date, media=None, media_type=None):
    if not text and not media:
        return
    caption = f"{text}\n\n📅 {date}" if text else f"📅 {date}"
    if media:
        print(f"Sending media ({media_type}): {media}")
        await post_media(bot, media_type, media, caption)
    else:
        print(f"Sending text: {caption}")
        await post_text(bot, caption)
    await asyncio.sleep(DELAY_SECONDS)

async def main():
    html_files = sorted([f for f in os.listdir(MEDIA_PATH) if f.startswith("messages") and f.endswith(".html")])

    for file in html_files:
        full_path = os.path.join(MEDIA_PATH, file)
        print(f"Processing file: {file}")
        with open(full_path, encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            messages = soup.find_all("div", class_="message")

            last_author_clean = None

            for msg in messages:
                author_tag = msg.find("div", class_="from_name")
                if author_tag:
                    author = author_tag.get_text(strip=True)
                    author_clean = author.strip().lower()
                    last_author_clean = author_clean
                else:
                    author_clean = last_author_clean

                # Select bot based on author
                if author_clean == AUTHOR_1:
                    bot = bot1
                elif author_clean == AUTHOR_2:
                    bot = bot2
                else:
                    bot = bot1  # fallback if unknown

                text_tag = msg.find("div", class_="text")
                date_tag = msg.find("div", class_="pull_right date details")
                text = text_tag.get_text(strip=True) if text_tag else ""
                if date_tag and 'title' in date_tag.attrs:
                    date = date_tag['title'].split(' UTC')[0]
                else:
                    date = "Unknown date"

                media_file = None
                media_type = None

                photo = msg.select_one("a.photo_wrap, div.media_photo a")
                video = msg.select_one("a.video_file_wrap, div.media_file a, a.video_file")
                voice = (
                    msg.find("a", class_="voice_message")
                    or msg.find("a", class_="audio_message")
                    or msg.find("a", class_="media_voice_message")
                )
                round_video = msg.find("a", class_="video_round_message")
                audio = msg.select_one("div.media_audio_file a")

                if photo and 'href' in photo.attrs:
                    media_file = os.path.join(MEDIA_PATH, photo['href'])
                    media_type = 'photo'
                elif video and 'href' in video.attrs:
                    media_file = os.path.join(MEDIA_PATH, video['href'])
                    media_type = 'video'
                elif voice and 'href' in voice.attrs:
                    media_file = os.path.join(MEDIA_PATH, voice['href'])
                    media_type = 'voice'
                elif round_video and 'href' in round_video.attrs:
                    media_file = os.path.join(MEDIA_PATH, round_video['href'])
                    media_type = 'video'
                elif audio and 'href' in audio.attrs:
                    media_file = os.path.join(MEDIA_PATH, audio['href'])
                    media_type = 'document'

                sticker = msg.find("div", class_="sticker_wrap")
                if sticker:
                    text += " [Sticker]"

                await process_message(bot, text, date, media_file, media_type)

        os.remove(full_path)
        print(f"Deleted processed file: {file}")

asyncio.run(main())
