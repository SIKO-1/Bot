# cmd_charge.py
from db_manager import update_user_gold
from aiogram import types

# 🆔 ايديات المطورين الثابتة
DEV_IDS = [5860391324, 7076215547, 7855813063]

COMMANDS = ["شحن"]

async def handle(bot, message: types.Message):
    if not message.text:
        return

    text = message.text.strip()
    parts = text.split()

    if parts[0] not in COMMANDS:
        return

    uid = message.from_user.id

    # 🔒 حماية: مطورين فقط
    if uid not in DEV_IDS:
        await message.reply("❌ هذا الأمر مخصص للمطورين فقط")
        return

    # =====================
    # حالة الرد على شخص
    # =====================
    if message.reply_to_message:
        if len(parts) != 2:
            await message.reply("⚠️ الصيغة:\nشحن <الكمية>")
            return

        try:
            amount = int(parts[1])
            if amount <= 0:
                raise ValueError
        except:
            await message.reply("❌ الكمية لازم تكون رقم أكبر من صفر")
            return

        target = message.reply_to_message.from_user
        new_gold = await update_user_gold(target.id, amount)

        await message.reply(
            f" تم الشحن بنجاح\n\n"
            f" الاسم: {target.first_name}\n"
            f" ID: {target.id}\n"
            f" المبلغ: +{amount}\n"
            f" الرصيد الحالي: {new_gold}"
        )
        return

    # =====================
    # حالة ID مباشر
    # =====================
    if len(parts) != 3:
        await message.reply(
            " الصيغة الصحيحة:\n"
            "شحن <ID> <الكمية>\n"
            "أو رد على الشخص واكتب:\n"
            "شحن <الكمية>"
        )
        return

    try:
        target_id = int(parts[1])
        amount = int(parts[2])
        if amount <= 0:
            raise ValueError
    except:
        await message.reply("❌ ID والكمية لازم يكونوا أرقام صحيحة والكميه أكبر من صفر")
        return

    new_gold = await update_user_gold(target_id, amount)

    await message.reply(
        f" تم شحن الحساب بنجاح\n\n"
        f" ID: {target_id}\n"
        f" المبلغ: +{amount}\n"
        f" الرصيد الحالي: {new_gold}"
    )
