import telebot

def handle(bot: telebot.TeleBot, message):
    text = message.text.strip().lower()
    if text == "هلا":
        bot.reply_to(message, "هلوات🫦")
