# ملف: cmd_youtube.py
import os
import io
import telebot
from pytube import YouTube
from youtubesearchpython import VideosSearch
import requests

COMMANDS = ["يوت"]

def handle(bot, message):
    text = message.text.strip()
    if not text.lower().startswith("يوت "):
        return

    query = text[4:].strip()
    chat_id = message.chat.id

    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت'")
        return

    msg = bot.send_message(chat_id, f"🔍 جاري البحث عن: {query}...")
    try:
        videos_search = VideosSearch(query, limit=1)
        result = videos_search.result()
        if not result['result']:
            bot.edit_message_text("❌ لم يتم العثور على الأغنية.", chat_id, msg.message_id)
            return

        video = result['result'][0]
        title = video['title']
        duration = video.get('duration', "غير معروف")
        thumbnail_url = video['thumbnails'][0]['url']
        video_url = video['link']

        # تحميل صورة الأغنية
        response = requests.get(thumbnail_url)
        img_bytes = io.BytesIO(response.content)

        # تحميل الصوت بصيغة MP3
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        audio_file = stream.download(filename=f"{yt.video_id}.mp4")
        mp3_file = f"{yt.video_id}.mp3"

        # تحويل MP4 إلى MP3 (إذا كان ffmpeg موجود)
        try:
            import moviepy.editor as mp
            clip = mp.AudioFileClip(audio_file)
            clip.write_audiofile(mp3_file)
            clip.close()
        except:
            mp3_file = audio_file  # fallback للملف الأصلي إذا لم يكن ffmpeg موجود

        # إرسال الأغنية
        bot.edit_message_text(f"🎵 تم العثور على الأغنية: {title}\n⏱ المدة: {duration}", chat_id, msg.message_id)
        bot.send_photo(chat_id, img_bytes, caption=f"🎶 {title}")
        bot.send_audio(chat_id, open(mp3_file, "rb"))

        # حذف الملفات المؤقتة
        try:
            os.remove(audio_file)
            if os.path.exists(mp3_file):
                os.remove(mp3_file)
        except:
            pass

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء البحث عن الأغنية:\n{str(e)}", chat_id, msg.message_id)
