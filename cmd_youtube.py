# cmd_youtube.py
import os
import tempfile
import traceback
from youtubesearchpython import VideosSearch
from pytube import YouTube
from telebot import types

def handle(bot, message):
    try:
        text = message.text.strip()
        if not text.lower().startswith("يوت "):
            return

        query = text[4:].strip()
        if not query:
            bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت'")
            return

        msg = bot.reply_to(message, "👑 الإمبراطور يبحث ويجهّز MP3...")

        # بحث أول نتيجة
        videosSearch = VideosSearch(query, limit=1)
        result = videosSearch.result()
        if not result["result"]:
            bot.edit_message_text("❌ ما تم العثور على الأغنية.", message.chat.id, msg.message_id)
            return

        video = result["result"][0]
        title = video["title"]
        thumbnail = video["thumbnails"][0]["url"]
        url = video["link"]

        bot.edit_message_text(f"🎵 وجدت الأغنية: {title}\n⏳ جاري التحميل...", message.chat.id, msg.message_id)

        # تحميل الفيديو مؤقتاً وتحويله MP3
        tmp_dir = tempfile.gettempdir()
        out_file = os.path.join(tmp_dir, f"{message.chat.id}.mp3")

        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=tmp_dir, filename=f"{message.chat.id}.mp4")

        # تحويل mp4 لـ mp3 باستخدام ffmpeg (يجب توفره على السيرفر)
        mp4_path = os.path.join(tmp_dir, f"{message.chat.id}.mp4")
        os.system(f"ffmpeg -y -i \"{mp4_path}\" -vn -ab 192k -ar 44100 -loglevel error \"{out_file}\"")
        os.remove(mp4_path)  # حذف الملف الأصلي بعد التحويل

        bot.edit_message_text(f"📤 جاري إرسال الأغنية: {title}", message.chat.id, msg.message_id)

        # إرسال الصوت + الغلاف
        audio = open(out_file, "rb")
        thumb_msg = types.InputMediaPhoto(thumbnail)
        bot.send_photo(message.chat.id, thumbnail, caption=f"🎵 {title}")
        bot.send_audio(message.chat.id, audio, title=title)
        audio.close()
        os.remove(out_file)

    except Exception as e:
        traceback.print_exc()
        bot.reply_to(message, f"❌ حدث خطأ: {e}")
