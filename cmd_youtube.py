import os
import telebot
import subprocess
import tempfile
import shutil

# ======================
# أمر cmd_youtube
# ======================
def handle(bot, message):
    if not message.text:
        return

    text = message.text.strip()
    if not text.lower().startswith("يوت "):
        return

    query = text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت'")
        return

    chat_id = message.chat.id
    sent = bot.send_message(chat_id, "👑 الإمبراطور يبحث ويجهّز الصوت...")

    # مجلد مؤقت للملفات
    temp_dir = tempfile.mkdtemp()
    audio_file = os.path.join(temp_dir, "audio.ogg")
    thumb_file = os.path.join(temp_dir, "thumb.jpg")

    try:
        # تحميل الصوت + الصورة باستخدام yt-dlp
        ytdlp_cmd = [
            "yt-dlp",
            f"ytsearch1:{query}",
            "-x", "--audio-format", "opus",
            "--audio-quality", "0",
            "--output", os.path.join(temp_dir, "%(id)s.%(ext)s"),
            "--write-thumbnail",
            "--no-playlist",
        ]
        subprocess.run(ytdlp_cmd, check=True)

        # العثور على الملفات داخل temp_dir
        audio_path = None
        thumb_path = None
        for f in os.listdir(temp_dir):
            if f.endswith(".opus"):
                audio_path = os.path.join(temp_dir, f)
            if f.endswith(".jpg"):
                thumb_path = os.path.join(temp_dir, f)

        if not audio_path:
            bot.edit_message_text("❌ حدث خطأ أثناء تجهيز الصوت.", chat_id, sent.message_id)
            return

        # اسم الأغنية من اسم الملف
        title = os.path.splitext(os.path.basename(audio_path))[0]

        # إرسال الصوت كـ Voice مع الصورة واسم الأغنية
        if thumb_path:
            with open(thumb_path, "rb") as img, open(audio_path, "rb") as audio:
                bot.send_voice(chat_id, audio, caption=f"🎵 {title}", thumb=img)
        else:
            with open(audio_path, "rb") as audio:
                bot.send_voice(chat_id, audio, caption=f"🎵 {title}")

        bot.delete_message(chat_id, sent.message_id)

    except subprocess.CalledProcessError:
        bot.edit_message_text("❌ حدث خطأ أثناء جلب الأغنية.", chat_id, sent.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: {e}", chat_id, sent.message_id)
    finally:
        shutil.rmtree(temp_dir)
