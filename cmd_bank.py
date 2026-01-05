# ملف: cmd_bank.py
import telebot
import db_manager

COMMANDS = ["بنك", "رصيد_بنك", "تحويل", "سحب", "ايداع", "احصائيات"]

def handle(bot, message):
    if not any(message.text.startswith(cmd) for cmd in COMMANDS):
        return

    uid = message.from_user.id
    user_name = message.from_user.first_name

    text = message.text

    # =========================
    # رصيد البنك
    # =========================
    if text in ["بنك", "رصيد_بنك"]:
        bank_gold = db_manager.get_user_bank(uid)
        bot.reply_to(message, f"💰 رصيدك في البنك: {bank_gold} ذهب")

    # =========================
    # إيداع
    # =========================
    elif text.startswith("ايداع"):
        parts = text.split()
        if len(parts) < 2:
            return bot.reply_to(message, "⚠️ اكتب المبلغ للإيداع، مثال: ايداع 500")
        try:
            amount = int(parts[1])
        except:
            return bot.reply_to(message, "❌ المبلغ يجب أن يكون رقم صحيح!")

        if amount <= 0:
            return bot.reply_to(message, "🚫 المبلغ يجب أن يكون أكبر من صفر!")

        user_gold = db_manager.get_user_gold(uid)
        if amount > user_gold:
            return bot.reply_to(message, f"⚠️ رصيدك الحالي {user_gold} ذهب فقط!")

        db_manager.update_user_gold(uid, -amount)
        db_manager.update_user_bank(uid, amount)
        bot.reply_to(message, f"✅ تم إيداع {amount} ذهب في البنك بنجاح!")

    # =========================
    # سحب
    # =========================
    elif text.startswith("سحب"):
        parts = text.split()
        if len(parts) < 2:
            return bot.reply_to(message, "⚠️ اكتب المبلغ للسحب، مثال: سحب 300")
        try:
            amount = int(parts[1])
        except:
            return bot.reply_to(message, "❌ المبلغ يجب أن يكون رقم صحيح!")

        bank_gold = db_manager.get_user_bank(uid)
        if amount > bank_gold:
            return bot.reply_to(message, f"⚠️ رصيدك في البنك {bank_gold} ذهب فقط!")

        db_manager.update_user_bank(uid, -amount)
        db_manager.update_user_gold(uid, amount)
        bot.reply_to(message, f"✅ تم سحب {amount} ذهب من البنك بنجاح!")

    # =========================
    # تحويل فلوس
    # =========================
    elif text.startswith("تحويل"):
        parts = text.split()
        if len(parts) < 3:
            return bot.reply_to(message, "⚠️ مثال للتحويل: تحويل 200 معرف_المستلم")
        try:
            amount = int(parts[1])
            target_id = int(parts[2])
        except:
            return bot.reply_to(message, "❌ المبلغ أو معرف المستلم غير صالح!")

        bank_gold = db_manager.get_user_bank(uid)
        if amount > bank_gold:
            return bot.reply_to(message, f"⚠️ رصيدك في البنك {bank_gold} ذهب فقط!")

        db_manager.update_user_bank(uid, -amount)
        db_manager.update_user_bank(target_id, amount)
        bot.reply_to(message, f"✅ تم تحويل {amount} ذهب إلى المستخدم {target_id} بنجاح!")

    # =========================
    # احصائيات البنك
    # =========================
    elif text == "احصائيات":
        total_gold = db_manager.get_total_gold()
        total_bank = db_manager.get_total_bank()
        bot.reply_to(message, f"📊 إحصائيات الإمبراطورية:\n💰 إجمالي الذهب: {total_gold}\n🏦 إجمالي الذهب في البنوك: {total_bank}")
