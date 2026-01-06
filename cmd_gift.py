import time
import db_manager

COMMANDS = ["هدية"]

# =========================
# دوال الهدايا اليومية
# =========================
def can_take_gift(uid):
    user = db_manager._get_user(uid)
    return time.time() - user.get("last_gift", 0) >= 86400

def take_gift(uid, amount=100):
    if not can_take_gift(uid):
        return None
    db_manager.update_user_gold(uid, amount)
    db_manager.users.update_one({"uid": uid}, {"$set": {"last_gift": time.time()}})
    return db_manager.get_user_gold(uid)

# =========================
# التعامل مع الأمر
# =========================
def handle(bot, message):
    if message.text not in COMMANDS:
        return

    uid = message.from_user.id

    # إذا يقدر ياخذ الهدية
    if can_take_gift(uid):
        amount = take_gift(uid)
        bot.reply_to(
            message,
            f"🎁 لقد استلمت هديتك اليومية!\n+{amount} ذهب 💰"
        )
        return

    # =========================
    # حساب الوقت المتبقي
    # =========================
    user = db_manager._get_user(uid)
    last_gift = user.get("last_gift", 0)

    now = time.time()
    remaining = int(86400 - (now - last_gift))  # 24 ساعة بالثواني
    if remaining < 0:
        remaining = 0

    hours = remaining // 3600
    minutes = (remaining % 3600) // 60
    seconds = remaining % 60  # لو تحب تستخدمها

    # =========================
    # الرد للانتظار
    # =========================
    bot.reply_to(
        message,
        f"⏳ انتظر قبل استلام هديتك القادمة:\n"
        f" {hours} ساعة و {minutes} دقيقة"
        # f" و {seconds} ثانية"  # لو حبيت تضيف الثواني
    )
