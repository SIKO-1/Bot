# ملف: cmd_youtube.py
import os
import tempfile
from pytube import Search, YouTube
from telebot import types

COMMANDS = ["يوت"]

def handle(bot, message):
    text = message.text.strip()
    if not text.lower().startswith("يوت "):
        return

    query = text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد 'يوت'")
        return

    msg = bot.send_message(message.chat.id, "🔎 جارٍ البحث عن الأغنية...")
    try:
        search = Search(query)
        result = search.results[0]  # أول نتيجة

        yt = YouTube(result.watch_url)
        title = yt.title
        thumbnail_url = yt.thumbnail_url

        # حفظ الصوت مؤقتاً
        temp_dir = tempfile.gettempdir()
        audio_stream = yt.streams.filter(only_audio=True).first()
        file_path = os.path.join(temp_dir, f"{title}.mp3")
        audio_stream.download(output_path=temp_dir, filename=f"{title}.mp3")

        # إرسال الصورة + الصوت + عنوان الإمبراطور
        caption = f"🎵 **{title}**\n👑 تم جلب الأغنية بأسلوب الإمبراطور!"
        bot.send_photo(message.chat.id, thumbnail_url, caption=caption, parse_mode="Markdown")
        with open(file_path, "rb") as f:
            bot.send_audio(message.chat.id, f, title=title)

        os.remove(file_path)  # تنظيف الملف بعد الإرسال
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.delete_message(message.chat.id, msg.message_id)
        bot.reply_to(message, f"❌ حدث خطأ أثناء البحث عن الأغنية:\n{e}")
