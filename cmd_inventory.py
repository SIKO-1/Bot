from db_manager import get_inventory

COMMANDS = ["مخزوني", "مقتنياتي"]

def handle(bot, message):
    if message.text not in COMMANDS:
        return

    uid = message.from_user.id
    inv = get_inventory(uid)
    if not inv:
        bot.reply_to(message, "📦 مخزونك فارغ حالياً")
        return

    text = "📦 مخزونك الحالي:\n" + "\n".join(f"- {item}" for item in inv)
    bot.reply_to(message, text)
