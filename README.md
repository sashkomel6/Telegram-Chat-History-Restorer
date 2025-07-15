# Telegram-Chat-History-Restorer
Python script for restoring and replaying exported Telegram chat history (HTML) into a channel using two separate bots, with media support and automatic file cleanup.
# Telegram Chat History Restorer

## 📖 Опис (Ukrainian)

Цей Python-скрипт автоматично відновлює історію переписки з HTML-архіву (`messagesX.html`), експортованого з Telegram Desktop, та надсилає повідомлення у Telegram-канал через двох окремих ботів.

Скрипт підтримує:
- текстові повідомлення
- фотографії
- відео
- голосові повідомлення (voice messages)
- стікери
- документи

Повідомлення розподіляються між двома ботами на основі автора повідомлення (автори налаштовуються вручну).

Після обробки кожного файлу `messagesX.html` він автоматично видаляється, щоб при повторному запуску скрипт не дублював вже надіслані повідомлення.

Скрипт також враховує `joined`-повідомлення (без явного автора) та правильно визначає їх автора за попереднім повідомленням.

## 🔧 Особливості
- Автоматичне відновлення та відправлення історії повідомлень
- Підтримка різних типів медіа
- Автоматичне видалення файлів після обробки
- Затримка між повідомленнями для обходу Flood Control
- Автоматичний retry при API-таймаутах та Flood Control
- Відображення дати без `UTC+02:00` у форматі `📅 dd.mm.yyyy hh:mm:ss`

## 🚀 Інструкція з використання

1️⃣ Експорт історії переписки в Telegram Desktop:
- Використайте "Export chat history" у Telegram Desktop.
- Оберіть формат HTML, обов’язково увімкніть завантаження медіафайлів (фото, відео, голосові).
- Скопіюйте файли `messages1.html`, `messages2.html` і всі медіа у каталог `/mnt/500hdd/tel`.

2️⃣ У скрипті вкажіть авторів:
Відкрийте HTML-файл, знайдіть `div class="from_name"`, скопіюйте точний текст для кожного автора і вставте в код:
```python
if author_clean == "author_1_name":
    bot = bot1
elif author_clean == "author_2_name":
    bot = bot2
else:
    bot = bot1
```

3️⃣ Укажіть токени ботів та ID каналу:
```python
SASHA_TOKEN = "<TOKEN Bot 1>"
YULIA_TOKEN = "<TOKEN Bot 2>"
CHANNEL_ID = <ID Telegram-каналу>
MEDIA_PATH = "/mnt/500hdd/tel"
```

4️⃣ Встановіть залежності:
```bash
pip install python-telegram-bot beautifulsoup4
```

5️⃣ Запустіть:
```bash
python3 restore_history.py
```

---

## 📖 Description (English)

This Python script automatically restores chat history from HTML archives (`messagesX.html`) exported by Telegram Desktop and sends the messages into a Telegram channel using two separate bots.

Supported content:
- Text messages
- Photos
- Videos
- Voice messages
- Stickers
- Documents

Messages are routed between two bots based on message author (authors must be configured manually).

After processing each `messagesX.html` file, it is automatically deleted to prevent duplicates during next runs.

The script also tracks the author for `joined` messages that don’t explicitly specify it.

## 🔧 Features
- Auto recovery and sending of chat history
- Media support
- Auto-delete processed files
- Delay between messages to avoid Flood Control
- Automatic retry on API timeouts and Flood Control
- Displays date without `UTC+02:00` in format `📅 dd.mm.yyyy hh:mm:ss`

## 🚀 Usage instructions

1️⃣ Export history from Telegram Desktop:
- Use "Export chat history".
- Choose HTML format and enable media export (photos, videos, voice).
- Copy `messages1.html`, `messages2.html` and all media files to `/mnt/500hdd/tel`.

2️⃣ Configure authors:
Open the HTML file, locate `div class="from_name"`, copy the exact text for each author and edit the script:
```python
if author_clean == "author_1_name":
    bot = bot1
elif author_clean == "author_2_name":
    bot = bot2
else:
    bot = bot1
```

3️⃣ Configure tokens and channel:
```python
SASHA_TOKEN = "<TOKEN Bot 1>"
YULIA_TOKEN = "<TOKEN Bot 2>"
CHANNEL_ID = <your channel ID>
MEDIA_PATH = "/mnt/500hdd/tel"
```

4️⃣ Install dependencies:
```bash
pip install python-telegram-bot beautifulsoup4
```

5️⃣ Run the script:
```bash
python3 restore_history.py
```

## ⚠️ Notes:
- Bots must be admins in the channel with post permissions.
- Ensure all referenced media files exist in the media folder.
- Telegram API timeouts cannot be disabled but script retries automatically.
- Files `messagesX.html` will be deleted after processing.

## 📝 License:
This project is provided for personal use. Be careful with sensitive data when deploying or sharing.

Author: anonymous — for Telegram users' convenience ❤️
