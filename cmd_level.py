# ملف: cmd_level.py
import math
from bot_config import db_manager
from aiogram import types

COMMANDS = ["مستوى", "لفلي", "lv"]

# ======= دالة لحساب المستوى بناءً على عدد الرسائل =======
def calculate_level(msg_count):
    level = 0
    remaining = msg_count
    base_required = 10  # الرسائل المطلوبة للمستوى الأول
    increment_factor = 1.5  # كل 10 مستويات يزيد الصعوبة

    while remaining >= base_required:
        remaining -= base_required
        level += 1
        # كل 10 مستويات يزيد المطلوب بنسبة تصاعدية
        if level % 10 == 0:
            base_required = math.ceil(base_required * increment_factor)

    return level, remaining, base_required

# ======= ألقاب حسب المستوى =======
def get_title(level):
    if level < 10:
        return "مبتدئ الإمبراطورية"
    elif level < 50:
        return "محارب الظل"
    elif level < 100:
        return "سيد الساحة"
    else:
        return "أسطورة كيرا"

# ======= التعامل مع أمر المستوى =======
async def handle(message: types.Message, bot):
    if not message.text:
        return
    text = message.text.strip().lower()
    if text not in COMMANDS:
        return

    uid = message.from_user.id

    # جلب عدد الرسائل السابقة من قاعدة البيانات
    msg_count = await db_manager.getUserMessageCount(uid)
    level_prev = await db_manager.getUserLevel(uid)

    # حساب المستوى الجديد
    level, remaining, next_req = calculate_level(msg_count)
    title = get_title(level)

    # حفظ المستوى الجديد
    await db_manager.setUserLevel(uid, level)

    # إذا ارتقى المستخدم عن مستواه السابق
    if level > level_prev:
        await bot.send_message(
            message.chat.id,
            f"🎉 مبروك {message.from_user.first_name}! لقد ارتقيت إلى المستوى {level} 🏆\n"
            f"لقبك الجديد: {title}"
        )

    # رسالة عامة عن المستوى الحالي
    text_msg = (
        "╔═════════════════╗\n"
        "      المستوى\n"
        "╚═════════════════╝\n\n"
        f"↫ مستواك ↫ {level}\n"
        f"↫ لقبك ↫ {title}\n"
        f"↫ عدد رسائلك ↫ {msg_count}\n"
        f"↫ للمستوى القادم ↫ {next_req - remaining} رسالة"
    )

    await bot.send_message(message.chat.id, text_msg)
