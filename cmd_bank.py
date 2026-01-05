# ملف: cmd_bank.py
import db_manager

COMMANDS = ["بنك", "رصيد_بنك", "سحب", "ايداع"]

def handle(bot, message):
    if not any(message.text.startswith(cmd) for cmd in COMMANDS):
        return

    uid = message.from_user.id
    text = message.text.strip()

    # =========================
    # رصيد البنك
    # =========================
    if text in ["بنك", "رصيد_بنك"]:
        bank_gold = db_manager.get_user_bank(uid)
        bot.reply_to(message, f"🏦 رصيدك في البنك: {bank_gold} ذهب")

    # =========================
    # إيداع
    # =========================
    elif text.startswith("ايداع"):
        parts = text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            return bot.reply_to(message, "⚠️ الصيغة: ايداع 500")

        amount = int(parts[1])

        if db_manager.deposit_to_bank(uid, amount):
            bot.reply_to(message, f"✅ تم إيداع {amount} ذهب في البنك")
        else:
            bot.reply_to(message, "❌ رصيدك لا يكفي")

    # =========================
    # سحب
    # =========================
    elif text.startswith("سحب"):
        parts = text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            return bot.reply_to(message, "⚠️ الصيغة: سحب 300")

        amount = int(parts[1])

        if db_manager.withdraw_from_bank(uid, amount):
            bot.reply_to(message, f"✅ تم سحب {amount} ذهب من البنك")
        else:
            bot.reply_to(message, "❌ رصيد البنك لا يكفي")
