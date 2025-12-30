import telebot
import os

# جلب التوكن من المتغيرات في ريلوي
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "هلا والله! أنا بوت شغال على Railway")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"أنت قلت: {message.text}")

# تشغيل البوت
if __name__ == "__main__":
    bot.infinity_polling()
