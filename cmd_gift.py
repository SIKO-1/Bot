from db_manager import take_gift, get_user_gold

COMMAND = "هدية"

def handle(bot, message):
    if message.text != COMMAND:
        return

    uid = message.from_user.id
    gold = take_gift(uid)

    if gold is not None:
        bot.reply_to(message, f"🎁 لقد حصلت على هديتك اليومية: +100 ذهب\n💰 رصيدك الحالي: {gold}")
    else:
        bot.reply_to(message, "🌚 لتصير طماع، تقدر أخذ الهدية مرة كل 24 ساعة بس ياطماع.")
