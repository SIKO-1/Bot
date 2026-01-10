# ملف: cmd_youtube.py
import os
from youtubesearchpython import VideosSearch
from pytube import YouTube
from telebot import types

COMMANDS = ["يوت"]

def handle(bot, message, *args):
    text = message.text.strip()
    if not text.lower().startswith("يوت "):
        return

    query = text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت'")
        return

    msg = bot.send_message(message.chat.id, "🔎 جاري البحث عن الأغنية...")
    try:
        # البحث عن الفيديو
        videos = VideosSearch(query, limit=1)
        result = videos.result()['result'][0]

        title = result['title']
        thumbnail = result['thumbnails'][0]['url']
        url = result['link']

        # تنزيل الصوت
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        safe_title = "".join(c for c in title if c.isalnum() or c in " -_")
        file_path = f"{safe_title}.mp3"
        audio_stream.download(filename=file_path)

        # إرسال الصورة مع العنوان
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔊 تحميل MP3", callback_data="noop"))
        bot.send_photo(
            message.chat.id,
            photo=thumbnail,
            caption=f"🎵 {title}\n📎 الرابط: {url}",
            reply_markup=markup
        )

        # إرسال الملف الصوتي
        with open(file_path, "rb") as f:
            bot.send_audio(message.chat.id, f, title=title)

        os.remove(file_path)  # حذف الملف بعد الإرسال
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"❌ حدث خطأ: {e}")
