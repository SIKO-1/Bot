# ملف: cmd_youtube.py
from youtubesearchpython import VideosSearch
from pytube import YouTube
import requests
import tempfile
import os
from db_manager import _get_user

COMMANDS = ["يوت"]

def handle(bot, message):
    text = message.text.strip()
    if not text.lower().startswith("يوت "):
        return

    query = text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت'")
        return

    msg = bot.send_message(message.chat.id, f"🔎 جاري البحث عن: {query} ...")
    try:
        # البحث عن الفيديو
        videosSearch = VideosSearch(query, limit=1)
        result = videosSearch.result()["result"]
        if not result:
            bot.edit_message_text("❌ لم يتم العثور على أي أغنية.", message.chat.id, msg.message_id)
            return

        video = result[0]
        title = video["title"]
        duration = video["duration"]
        thumbnail_url = video["thumbnails"][0]["url"]
        video_url = video["link"]

        # تحميل الصوت مؤقتًا
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio_stream.download(output_path=os.path.dirname(temp_file.name), filename=os.path.basename(temp_file.name))

        # إرسال صورة + صوت
        bot.send_photo(message.chat.id, photo=thumbnail_url, caption=f"🎵 {title}\n⏱️ {duration}")
        with open(temp_file.name, "rb") as f:
            bot.send_audio(message.chat.id, f)

        os.remove(temp_file.name)
        bot.edit_message_text(f"✅ تم تحميل الأغنية: {title}", message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: {e}", message.chat.id, msg.message_id)
