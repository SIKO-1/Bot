# ملف: cmd_youtube.py
import os
import re
import subprocess
import tempfile
from telebot import types
from yt_dlp import YoutubeDL
import shutil

COMMANDS = ["يوت"]

YDL_OPTS = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "outtmpl": "",  # سيتم تحديده وقت التحميل
    "quiet": True,
    "noplaylist": True,
}

def search_youtube(query):
    safe_query = re.sub(r"[^\w\s]", "", query)
    return f"ytsearch1:{safe_query}"

def download_audio(query, chat_id):
    tmpdir = tempfile.mkdtemp(prefix="ytmp3_")  # مجلد مؤقت ثابت
    mp3_path = os.path.join(tmpdir, f"{chat_id}.mp3")
    YDL_OPTS["outtmpl"] = mp3_path
    try:
        with YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(search_youtube(query), download=True)
            if "entries" in info:
                entry = info["entries"][0]
                title = entry.get("title")
                thumbnail = entry.get("thumbnail")
            else:
                title = info.get("title")
                thumbnail = info.get("thumbnail")
        return mp3_path, title, thumbnail, tmpdir
    except Exception as e:
        shutil.rmtree(tmpdir, ignore_errors=True)
        return None, None, None, None

def handle(bot, message, cmd_modules=None, game_modules=None, module_errors=None):
    text = message.text.strip()
    chat_id = message.chat.id

    if not text.lower().startswith("يوت "):
        return

    query = text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت'")
        return

    sent_msg = bot.send_message(chat_id, "👑 الإمبراطور يبحث ويجهّز MP3...")

    mp3_path, title, thumbnail, tmpdir = download_audio(query, chat_id)

    if not mp3_path or not os.path.isfile(mp3_path):
        bot.edit_message_text("❌ حدث خطأ أثناء جلب الأغنية.", chat_id, sent_msg.message_id)
        return

    caption = f"🎵 {title}" if title else "🎵 أغنية جاهزة"

    # إرسال الغلاف أولاً
    if thumbnail:
        try:
            bot.send_photo(chat_id, thumbnail, caption=caption)
        except:
            pass

    # إرسال الصوت
    try:
        with open(mp3_path, "rb") as f:
            bot.send_audio(chat_id, f, title=title)
    except Exception as e:
        bot.send_message(chat_id, f"❌ حدث خطأ أثناء إرسال الصوت: {e}")

    # تنظيف الملفات بعد الإرسال
    shutil.rmtree(tmpdir, ignore_errors=True)
    bot.delete_message(chat_id, sent_msg.message_id)
