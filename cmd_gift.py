# ملف: cmd_gift.py
from datetime import datetime, timedelta
from db_manager import get_user, update_user_gold
from aiogram import types

COMMANDS = ["هدية"]
DAY = timedelta(hours=24)  # مدة الانتظار 24 ساعة

# =========================
# التحقق إذا المستخدم يقدر ياخذ هديته
# =========================
async def can_take_gift(uid):
    user = await get_user(uid)
    last_gift_time = user.get("last_gift_time", None)
    if not last_gift_time:
        return True
    last_gift = datetime.fromtimestamp(last_gift_time)
    return datetime.now() - last_gift >= DAY

# =========================
# استلام الهدية
# =========================
async def take_gift(uid, amount=100):
    if not await can_take_gift(uid):
        return None
    await update_user_gold(uid, amount)
    # تحديث وقت آخر هدية
    user = await get_user(uid)
    user["last_gift_time"] = datetime.now().timestamp()
    # هنا لو تستخدم قاعدة بيانات فعلية احفظ الوقت فيها
    return await get_user(uid)["gold"]

# =========================
# التعامل مع الأمر
# =========================
async def handle(message: types.Message, bot):
    text = message.text.strip()
    if text not in COMMANDS:
        return

    uid = message.from_user.id

    if await can_take_gift(uid):
        amount = await take_gift(uid)
        await bot.send_message(
            message.chat.id,
            f"🎁 لقد استلمت هديتك اليومية!\n+{amount} ذهب 💰\n✨ مفاجأة اليوم لك!"
        )
        return

    # =========================
    # حساب الوقت المتبقي
    # =========================
    user = await get_user(uid)
    last_gift_time = user.get("last_gift_time", 0)
    last_gift = datetime.fromtimestamp(last_gift_time)
    remaining = DAY - (datetime.now() - last_gift)
    if remaining.total_seconds() < 0:
        remaining = timedelta(seconds=0)

    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60
    await bot.send_message(
        message.chat.id,
        f"⏳ انتظر قبل استلام هديتك القادمة:\n {hours} ساعة و {minutes} دقيقة"
    )
