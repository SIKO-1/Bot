import os
import telebot
import subprocess
import tempfile

def handle(bot, message):
    if not message.text or not message.text.lower().startswith("يوت "):
        return

    query = message.text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت '")
        return

    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "👑 الإمبراطور يبحث ويجهّز الصوت...")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # ملف صوتي بصيغة ogg (voice)
            out_file = os.path.join(tmpdir, f"{chat_id}.ogg")
            
            # yt-dlp لتحميل أول نتيجة وتحويلها إلى ogg
            cmd = [
                "yt-dlp",
                f"ytsearch1:{query}",
                "-x",
                "--audio-format", "opus",  # opus مناسب كـ voice note
                "-o", out_file,
                "--no-playlist"
            ]
            subprocess.run(cmd, check=True)

            # إرسال كـ voice note
            with open(out_file, "rb") as audio:
                bot.send_voice(chat_id, audio)
        
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء جلب الصوت:\n{e}", chat_id, msg.message_id)
