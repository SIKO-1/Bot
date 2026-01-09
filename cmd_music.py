# ملف: cmd_music.py
import telebot
import os
import random

COMMANDS = ["ميوزك", "اغنيه", "اغاني"]

# مجلد الأصوات
voices_folder = os.path.join(os.path.dirname(__file__), "voices")
all_files = [os.path.join(voices_folder, f) for f in os.listdir(voices_folder) if f.endswith(".ogg")]

def handle(bot, message):
    if message.text not in COMMANDS:
        return
    if not all_files:
        bot.reply_to(message, "⚠️ ماكو أي ملف صوت متوفر!")
        return
    audio_file = random.choice(all_files)
    with open(audio_file, "rb") as f:
        bot.send_audio(message.chat.id, f)
