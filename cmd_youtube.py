# cmd_youtube.py
import os
import subprocess
from youtubesearchpython import VideosSearch

def handle(bot, message):
    if not message.text:
        return

    if not message.text.startswith("يوت "):
        return

    query = message.text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد كلمة يوت")
        return

    chat_id = message.chat.id

    try:
        bot.send_message(chat_id, "🔎 الإمبراطور يبحث عن الأغنية...")

        search = VideosSearch(query, limit=1)
        result = search.result()["result"]

        if not result:
            bot.reply_to(message, "❌ ما لقيت شي بهالاسم")
            return

        video = result[0]
        title = video["title"]
        url = video["link"]
        thumb = video["thumbnails"][0]["url"]

        bot.send_photo(chat_id, thumb, caption=f"🎧 {title}\n⏳ جاري التحميل MP3...")

        output_file = f"/tmp/{chat_id}.mp3"

        command = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", output_file,
            url
        ]

        subprocess.run(command, check=True)

        with open(output_file, "rb") as audio:
            bot.send_audio(
                chat_id,
                audio,
                title=title
            )

        os.remove(output_file)

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ:\n{e}")
