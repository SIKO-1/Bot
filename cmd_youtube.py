import os
import subprocess
from telebot import types

def handle(bot, message):
    if not message.text:
        return

    text = message.text.strip()
    if not text.startswith("يوت "):
        return

    query = text[4:].strip()
    chat_id = message.chat.id

    # إرسال رسالة مؤقتة
    temp_msg = bot.send_message(chat_id, "👑 الإمبراطورية تبحث وتجهّز MP3...")

    # ملف مؤقت على السيرفر
    output_path = f"/tmp/{chat_id}.mp3"

    try:
        # yt-dlp ينزل الأغنية فقط بصيغة mp3
        subprocess.run([
            "yt-dlp",
            f"ytsearch1:{query}",
            "-x",
            "--audio-format", "mp3",
            "-o", output_path,
            "--no-playlist"
        ], check=True)

        # إرسال الصوت
        with open(output_path, "rb") as audio:
            bot.send_audio(chat_id, audio)

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء جلب الأغنية.")

    finally:
        # حذف الرسالة المؤقتة
        try:
            bot.delete_message(chat_id, temp_msg.message_id)
        except:
            pass

        # حذف الملف المؤقت
        if os.path.exists(output_path):
            os.remove(output_path)
