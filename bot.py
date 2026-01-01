import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # تأكد إن اسم المتغير BOT_TOKEN صحيح
bot = telebot.TeleBot(TOKEN)
