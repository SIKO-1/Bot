# cmd_marriage.py
import random
from db_manager import users_col, get_user

# ======= إعداد الزواج =======
marriage_enabled = True

async def is_already_married(uid):
    marriage = await users_col.find_one({
        "$or": [{"husband_uid": uid}, {"wife_uid": uid}]
    })
    return marriage is not None

async def get_marriage(uid):
    return await users_col.find_one({
        "$or": [{"husband_uid": uid}, {"wife_uid": uid}]
    })

# ======= أمر زوجني =======
async def marry_user(bot, message, target_identifier=None):
    user = await get_user(message.from_user.id, message.from_user.first_name)

    if await is_already_married(user["uid"]):
        await bot.send_message(message.chat.id, f"⚠️ {user['name']} أنت متزوج بالفعل!")
        return

    target_user = None

    # ===== إذا رد على شخص =====
    if message.reply_to_message:
        target_user = await get_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)
    # ===== إذا ذكر UID أو @username =====
    elif target_identifier:
        if target_identifier.startswith("@"):
            target_user = await users_col.find_one({"username": target_identifier[1:]})
        else:
            try:
                target_uid = int(target_identifier)
                target_user = await get_user(target_uid)
            except:
                await bot.send_message(message.chat.id, "⚠️ الرجاء كتابة UID صالح أو @username")
                return
    # ===== بدون أي تحديد =====
    if not target_user:
        all_users = await users_col.find({"uid": {"$ne": user["uid"]}}).to_list(length=None)
        if not all_users:
            await bot.send_message(message.chat.id, "⚠️ لا يوجد مستخدمين آخرين في قاعدة البيانات!")
            return
        target_user = random.choice(all_users)

    if await is_already_married(target_user["uid"]):
        await bot.send_message(message.chat.id, f"⚠️ {target_user['name']} هذا الشخص متزوج بالفعل!")
        return

    # تسجيل الزواج
    await users_col.insert_one({
        "husband_uid": user["uid"],
        "wife_uid": target_user["uid"],
        "married_at": int(message.date.timestamp())
    })

    text = f"💍 تم الزواج بنجاح بين:\n• {user['name']} ❤️ {target_user['name']}"
    meme_url = "https://i.imgur.com/9bX5YUw.jpg"
    await bot.send_photo(message.chat.id, meme_url, caption=text)

# ======= أمر طلقني =======
async def divorce(bot, message):
    user = await get_user(message.from_user.id, message.from_user.first_name)
    marriage = await get_marriage(user["uid"])
    if not marriage:
        await bot.send_message(message.chat.id, f"⚠️ {user['name']} أنت غير متزوج حالياً!")
        return

    await users_col.delete_one({"_id": marriage["_id"]})
    await bot.send_message(message.chat.id, f"💔 {user['name']} تم الطلاق بنجاح!")

# ======= قائمة المتزوجين =======
async def list_married(bot, message):
    all_marriages = await users_col.find({"husband_uid": {"$exists": True}}).to_list(length=None)
    if not all_marriages:
        await bot.send_message(message.chat.id, "لا يوجد متزوجين حالياً.")
        return

    text = "💑 قائمة المتزوجين:\n"
    for m in all_marriages:
        husband = await get_user(m["husband_uid"])
        wife = await get_user(m["wife_uid"])
        text += f"• {husband['name']} ❤️ {wife['name']}\n"

    await bot.send_message(message.chat.id, text)

# ======= Handler =======
async def handle(bot, message):
    if not marriage_enabled:
        return

    text = message.text
    if not text:
        return

    parts = text.strip().split()
    command = parts[0]
    target_identifier = parts[1] if len(parts) > 1 else None

    if command == "زوجني":
        await marry_user(bot, message, target_identifier)
    elif command == "طلقني":
        await divorce(bot, message)
    elif command == "قائمة المتزوجين":
        await list_married(bot, message)
