import os
import subprocess

def handle(bot, message):
    if not message.text:
        return

    text = message.text.strip()
    if not text.startswith("يوت "):
        return

    query = text[4:].strip()
    chat_id = message.chat.id

    temp_msg = bot.send_message(chat_id, "👑 الإمبراطورية تبحث وتجهّز MP3...")

    output_path = f"/tmp/{chat_id}.mp3"

    try:
        # yt-dlp يبحث أول نتيجة وينزل MP3 فقط
        subprocess.run([
            "yt-dlp",
            f"ytsearch1:{query}",
            "-x",
            "--audio-format", "mp3",
            "-o", output_path,
            "--no-playlist"
        ], check=True)

        with open(output_path, "rb") as audio:
            bot.send_audio(chat_id, audio)

    except Exception as e:
        bot.reply_to(message, "❌ حدث خطأ أثناء جلب الأغنية.")

    finally:
        try:
            bot.delete_message(chat_id, temp_msg.message_id)
        except:
            pass

        if os.path.exists(output_path):
            os.remove(output_path)
