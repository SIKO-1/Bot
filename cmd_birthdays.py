# cmd_birthdays.py
import asyncio
import random
from datetime import datetime
from aiogram import types
from db_manager import (
    add_birthday,
    remove_birthday,
    get_birthday,
    list_birthdays,
    enable_birthday_auto,
    disable_birthday_auto,
    is_birthday_auto_enabled
)

COMMANDS = [
    "اضف عيد",
    "مسح عيد",
    "عيد ميلاد",
    "قائمه الاعياد",
    "تفعيل عيد ميلاد",
    "تعطيل عيد ميلاد",
    "زواج"
]

CHECK_INTERVAL = 300  # 5 دقائق

# ===========================
# معالجة الرسائل
# ===========================
async def handle(bot, message: types.Message):
    text = message.text.strip()
    uid = message.from_user.id

    # ===== إضافة عيد =====
    if text.startswith("اضف عيد"):
        parts = text.split()
        if len(parts) < 5:
            await message.reply("❌ الصيغة: اضف عيد <ID> <اليوم> <الشهر> [السنة]")
            return

        target_uid = int(parts[2])
        day = int(parts[3])
        month = int(parts[4])
        year = int(parts[5]) if len(parts) > 5 else None

        res = await add_birthday(target_uid, day, month, year)
        if res.get("ok"):
            await message.reply(f"✅ تم إضافة عيد الميلاد\nUID: {target_uid}\n📅 {day}/{month}/{year or '؟'}")
        else:
            await message.reply(res.get("error", "❌ خطأ أثناء الإضافة"))
        return

    # ===== مسح عيد =====
    if text.startswith("مسح عيد"):
        parts = text.split()
        if len(parts) < 3:
            await message.reply("❌ الصيغة: مسح عيد <ID>")
            return
        await remove_birthday(int(parts[2]))
        await message.reply("✅ تم مسح عيد الميلاد")
        return

    # ===== عرض عيد =====
    if text.startswith("عيد ميلاد"):
        parts = text.split()
        if len(parts) < 3:
            await message.reply("❌ الصيغة: عيد ميلاد <ID>")
            return

        bd = await get_birthday(int(parts[2]))
        if not bd:
            await message.reply("⚠️ ما مسجل عيد ميلاد")
            return

        await message.reply(f"🎂 عيد الميلاد:\n📅 {bd['day']}/{bd['month']}/{bd.get('year','؟')}")
        return

    # ===== قائمة الاعياد =====
    if text == "قائمه الاعياد":
        birthdays = await list_birthdays()
        if not birthdays:
            await message.reply("⚠️ ماكو أعياد مسجلة")
            return

        msg = "🎉 قائمة الأعياد:\n\n"
        for b in birthdays:
            bd = b['birthday']
            msg += f"• {b['uid']} → {bd['day']}/{bd['month']}/{bd.get('year','؟')}\n"
        await message.reply(msg)
        return

    # ===== تفعيل / تعطيل =====
    if text == "تفعيل عيد ميلاد":
        await enable_birthday_auto(uid)
        await message.reply("✅ تم التفعيل")
        return

    if text == "تعطيل عيد ميلاد":
        await disable_birthday_auto(uid)
        await message.reply("🚫 تم التعطيل")
        return

    # ===== زواج =====
    if text == "زواج":
        if not message.reply_to_message:
            await message.reply("💍 رد على رسالة الشخص حتى أزوجكم 😏")
            return

        user1 = message.from_user.first_name
        user2 = message.reply_to_message.from_user.first_name

        captions = [
            f"💍 مبروك الزواج!\n{user1} ❤️ {user2}\nالله بالخير 👰🤵",
            f"😂 تم عقد القِران!\n{user1} × {user2}\nزواج ميمز رسمي",
            f"👑 زوجين VIP\n{user1} 🤍 {user2}"
        ]

        caption = random.choice(captions)
        await message.reply(caption)
        return

# ===========================
# جدولة تهاني عيد الميلاد
# ===========================
async def birthday_scheduler(bot):
    while True:
        today = datetime.today()
        birthdays = await list_birthdays()

        for b in birthdays:
            bd = b["birthday"]
            if bd["day"] == today.day and bd["month"] == today.month:
                if not await is_birthday_auto_enabled(b["uid"]):
                    continue

                try:
                    # ===== رسالة خاصة مع صورة عيد ميلاد تلقائية =====
                    img_path = f"assets/birthday_{random.randint(1,5)}.jpg"  # صور مخصصة 1-5
                    caption = f"🎉 كل عام وأنت بخير!\n🎂 عيد ميلاد سعيد"
                    await bot.send_photo(b["uid"], photo=open(img_path, "rb"), caption=caption)

                    # ===== ميزة مميزة: رسالة جماعية في المجموعات =====
                    # لو تضيف قاعدة بيانات بالمجموعات لكل UID، نقدر نفعل التالي:
                    # for group_id in await get_user_groups(b["uid"]):
                    #     await bot.send_message(group_id, f"🎉 اليوم عيد ميلاد {b['uid']}! 🎂")
                except:
                    continue

        await asyncio.sleep(CHECK_INTERVAL)
