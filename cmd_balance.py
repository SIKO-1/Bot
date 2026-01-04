from db_manager import get_user_gold

COMMANDS = ["فلوسي", "فلوس", "رصيدي", "رصيدي"]

def handle(bot, message):
    if message.text not in COMMANDS:
        return

    uid = message.from_user.id
    gold = get_user_gold(uid)
    bot.reply_to(message, f"💰 رصيدك الحالي: {gold} ذهب")
