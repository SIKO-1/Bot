from db_manager import take_gift, can_take_gift

COMMANDS = ["هدية"]

def handle(bot, message):
    if message.text not in COMMANDS:
        return

    uid = message.from_user.id
    if can_take_gift(uid):
        amount = take_gift(uid)
        bot.reply_to(message, f"🎁 لقد استلمت هديتك اليومية! +{amount} ذهب")
    else:
        bot.reply_to(message, "⏳ لم يحن وقت الهدية بعد، انتظر 24 ساعة من آخر هدية.")
