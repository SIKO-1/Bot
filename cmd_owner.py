from aiogram import types

COMMANDS = ["المالك"]

async def handle(bot, message: types.Message):
    try:
        # تحقق أساسي
        if not message or not message.text:
            return

        if message.text.strip() not in COMMANDS:
            return

        chat_id = message.chat.id

        # جلب الأدمنز
        try:
            admins = await bot.get_chat_administrators(chat_id)
        except:
            await message.reply("⌁︙لا أملك صلاحية الوصول لمعلومات الإدارة")
            return

        owner = None
        for admin in admins:
            if admin.status == "creator":
                owner = admin.user
                break

        if not owner:
            await message.reply("⌁︙تعذر العثور على مالك المجموعة")
            return

        # بيانات آمنة (مهما كان)
        name = owner.first_name or "Unknown"
        username = f"@{owner.username}" if owner.username else "None"
        bio = "None"

        # محاولة جلب البايو
        try:
            full = await bot.get_chat(owner.id)
            if full.bio:
                bio = full.bio
        except:
            pass

        text = (
            f"⤠ 𝑵𝒂𝒎𝒆: {name}\n"
            f"⤠ 𝑼𝒔𝒆𝒓: {username}\n"
            f"⤠ 𝑩𝒊𝒐: {bio}"
        )

        # محاولة إرسال صورة
        try:
            photos = await bot.get_user_profile_photos(owner.id, limit=1)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                await bot.send_photo(chat_id, photo=file_id, caption=text)
                return
        except:
            pass

        # fallback نص فقط
        await message.reply(text)

    except:
        # صامت 100% — مستحيل يطيح البوت
        return
