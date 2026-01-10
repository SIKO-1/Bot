# ملف: cmd_youtube.py
import telebot
from pytube import YouTube
from youtube_search import YoutubeSearch
import requests
from io import BytesIO

COMMANDS = ["يوت"]

def handle(bot, message):
    text = message.text
    chat_id = message.chat.id

    if not text.startswith("يوت "):
        return

    query = text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت'")
        return

    try:
        # البحث عن الفيديو
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            bot.reply_to(message, "❌ ما حصلت أي أغنية لهذا الاسم.")
            return

        video = results[0]
        video_url = f"https://www.youtube.com{video['url_suffix']}"
        title = video['title']
        thumbnail_url = video['thumbnails'][0]

        # تحميل الصورة
        try:
            thumb_data = requests.get(thumbnail_url, timeout=10).content
            thumb_file = BytesIO(thumb_data)
            thumb_file.name = "thumb.jpg"
        except:
            thumb_file = None

        # تحميل الصوت (MP4) بشكل خفيف
        try:
            yt = YouTube(video_url)
            stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
            if not stream:
                bot.reply_to(message, "❌ ما قدر أحصل الصوت.")
                return
            # الحد الأقصى لحجم الملف: 15 ميجا (Railway غالبًا يسمح)
            if stream.filesize_approx and stream.filesize_approx > 15*1024*1024:
                bot.reply_to(message, "❌ حجم الأغنية كبير جدًا، حاول بأغنية أصغر.")
                return
            audio_data = stream.stream_to_buffer()
            audio_data.seek(0)
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ أثناء تحميل الصوت:\n{e}")
            return

        # إرسال الصورة + الصوت
        caption = f"🎵 {title}\n📎 [رابط اليوتيوب]({video_url})"
        if thumb_file:
            bot.send_photo(chat_id, thumb_file, caption=caption, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, caption, parse_mode="Markdown")

        bot.send_audio(chat_id, audio_data, title=title)

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ:\n{e}")
