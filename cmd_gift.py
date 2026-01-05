import time
import db_manager
from db_manager import take_gift, can_take_gift

COMMANDS = ["هدية"]

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
    user = db_manager.users.find_one({"uid": uid})
    last_gift = user.get("last_gift", 0)

    now = time.time()
    remaining = int(86400 - (now - last_gift))  # 24 ساعة بالثواني

    if remaining < 0:
        remaining = 0

    hours = remaining // 3600
    minutes = (remaining % 3600) // 60
    seconds = remaining % 60  # لو حبيت تستخدمها

    # =========================
    # الرد الوقح اللطيف 😈
    # =========================
    bot.reply_to(
        message,
        f"ياطماع 🌚 انتظر بعد:\n"
        f" {hours} ساعة و {minutes} دقيقة"
        # لو تحب تضيف ثواني:
        # f" و {seconds} ثانية"
    )
