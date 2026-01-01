import telebot
import os

# التوكن يقرأ من متغير البيئة فقط
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
