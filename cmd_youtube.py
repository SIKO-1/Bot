# ملف: cmd_youtube.py
import os
import traceback
import requests
from youtubesearchpython import VideosSearch
from pytube import YouTube
from io import BytesIO
import db_manager

COMMANDS = ["يوت"]

def handle(bot, message):
    text = message.text.strip()
    uid = message.from_user.id

    if not text.startswith("يوت "):
        return

    query = text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت'")
        return

    try:
        bot.send_message(message.chat.id, f"🔎 جاري البحث عن: {query} ...")

        # البحث عن الفيديو
        videosSearch = VideosSearch(query, limit=1)
        result = videosSearch.result()
        if not result["result"]:
            bot.reply_to(message, "⚠️ لم يتم العثور على أي فيديو.")
            return

        video = result["result"][0]
        video_title = video["title"]
        video_link = video["link"]
        video_thumbnail = video["thumbnails"][0]["url"]

        # تحميل الفيديو كـ MP3
        bot.send_message(message.chat.id, f"⏬ جاري تحميل: {video_title} ...")
        yt = YouTube(video_link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        buffer = BytesIO()
        audio_stream.stream_to_buffer(buffer)
        buffer.seek(0)

        # إرسال الغلاف + اسم الأغنية + الملف
        bot.send_photo(
            message.chat.id,
            photo=video_thumbnail,
            caption=f"🎵 {video_title}"
        )
        bot.send_audio(
            message.chat.id,
            audio=buffer,
            title=video_title,
            performer=yt.author
        )

    except Exception as e:
        traceback.print_exc()
        bot.reply_to(message, f"❌ حدث خطأ أثناء جلب الأغنية:\n{e}")
