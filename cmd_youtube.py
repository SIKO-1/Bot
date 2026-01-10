import os
import subprocess
import json
import requests

COMMANDS = ["يوت"]

def handle(bot, message):
    if not message.text.startswith("يوت"):
        return

    query = message.text.replace("يوت", "", 1).strip()
    if not query:
        bot.reply_to(message, "❌ اكتب اسم الأغنية بعد الأمر.")
        return

    chat_id = message.chat.id

    try:
        # ===== 1. جلب معلومات الفيديو (JSON) =====
        info_cmd = [
            "yt-dlp",
            f'ytsearch1:"{query}"',
            "--dump-single-json",
            "--no-playlist"
        ]

        info = subprocess.check_output(info_cmd, text=True)
        data = json.loads(info)

        title = data.get("title", "أغنية")
        thumbnail = data.get("thumbnail")
        video_url = data.get("webpage_url")

        # ===== 2. تحميل الصوت =====
        audio_path = f"/tmp/{chat_id}.mp3"

        download_cmd = [
            "yt-dlp",
            video_url,
            "-x",
            "--audio-format",
            "mp3",
            "-o",
            audio_path
        ]

        subprocess.run(download_cmd, check=True)

        # ===== 3. تحميل الصورة =====
        photo_path = f"/tmp/{chat_id}.jpg"
        if thumbnail:
            img = requests.get(thumbnail, timeout=10).content
            with open(photo_path, "wb") as f:
                f.write(img)

            bot.send_photo(
                chat_id,
                open(photo_path, "rb"),
                caption=f"🎧 **{title}**\n👑 Imperial Music"
            )

        # ===== 4. إرسال الصوت =====
        bot.send_audio(
            chat_id,
            open(audio_path, "rb"),
            title=title,
            caption="🎶 تم التحميل بواسطة الإمبراطور"
        )

        # تنظيف
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(photo_path):
            os.remove(photo_path)

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ:\n{e}")
