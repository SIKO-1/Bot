# cmd_youtube.py
import os
import subprocess

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
        bot.send_message(chat_id, "👑 الإمبراطور يبحث ويجهّز MP3...")

        output = f"/tmp/{chat_id}.mp3"

        command = [
            "yt-dlp",
            f"ytsearch1:{query}",
            "-x",
            "--audio-format", "mp3",
            "-o", output,
            "--no-playlist"
        ]

        subprocess.run(command, check=True)

        with open(output, "rb") as audio:
            bot.send_audio(chat_id, audio, caption=f"🎧 {query}")

        os.remove(output)

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ:\n{e}")
