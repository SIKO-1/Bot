from bot import bot

@bot.message_handler(func=lambda message: message.text == "مرحبا")
def hello(message):
    bot.reply_to(message, "أهلاً بك في إمبراطورية كرار 👑")
