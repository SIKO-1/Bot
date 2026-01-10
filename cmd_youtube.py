# cmd_youtube.py
import os
import subprocess
import telebot
from youtube_search import YoutubeSearch
import requests
from tempfile import mkdtemp

def handle(bot, message):
    text = message.text.strip()
    if not text.lower().startswith("يوت "):
        return

    query = text[4:].strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد الأمر 'يوت'")
        return

    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "👑 الإمبراطور يبحث ويجهّز MP3...")

    try:
        # بحث عن أول نتيجة على يوتيوب
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            bot.edit_message_text("❌ لم يتم العثور على الأغنية.", chat_id, msg.message_id)
            return

        video = results[0]
        video_url = f"https://www.youtube.com{video['url_suffix']}"
        title = video['title']
        thumb_url = video['thumbnails'][0]

        # تحميل صورة الغلاف
        thumb_data = requests.get(thumb_url).content

        # حفظ مؤقت
        tmp_dir = mkdtemp()
        mp3_path = os.path.join(tmp_dir, f"{chat_id}.mp3")
        thumb_path = os.path.join(tmp_dir, f"{chat_id}.jpg")

        with open(thumb_path, "wb") as f:
            f.write(thumb_data)

        # تحميل الصوت بصيغة MP3
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--restrict-filenames",
            "--no-check-certificate",
            video_url,
            "-o", mp3_path,
            "--no-playlist"
        ]
        subprocess.run(cmd, check=True)

        if not os.path.exists(mp3_path):
            bot.edit_message_text("❌ حدث خطأ أثناء جلب الأغنية.", chat_id, msg.message_id)
            return

        # إرسال الغلاف
        bot.send_photo(chat_id, open(thumb_path, "rb"), caption=f"🎵 {title}")

        # إرسال الصوت
        bot.send_audio(chat_id, open(mp3_path, "rb"), title=title)

        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: {e}", chat_id, msg.message_id)
