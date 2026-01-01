import telebot
import os
from db_manager import get_user, update_user
# استيراد الأوامر من الملفات الأخرى
from cmd_gift import register_gift_handler

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# تسجيل الأوامر
register_gift_handler(bot)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ البوت يعمل بنظام الذاكرة الدائمة!")

bot.polling(none_stop=True)
