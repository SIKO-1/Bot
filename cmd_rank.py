import asyncio
from aiogram import types
from db_manager import (
    get_user_rank, set_user_rank,
    get_user_gold, update_user_gold,
    add_special_user, list_special_users,
)

# ======================
# إعدادات الرتب
# ======================
MAX_RANK = 10
RANKS = {
    0: ["بدون رتبة", 0],
    1: ["مبتدئ", 100],
    2: ["متقدم", 300],
    3: ["محترف", 600],
    4: ["خبير", 1000],
    5: ["قائد فريق", 1500],
    6: ["نجم", 2200],
    7: ["مميز", 3000],
    8: ["VIP", 4000],
    9: ["سوبر VIP", 5500],
    10: ["مشرف البوت", None],  # أعلى رتبة - يعطي مشرف تلقائي بالمجموعة
}

# قائمة المستخدمين المميزين (UID)
SPECIAL_USERS = set()

# ======================
# التعامل مع الرتب
# ======================
async def handle(bot, message: types.Message, is_group: bool = True):
    text = message.text.strip()
    uid = message.from_user.id
    chat_id = message.chat.id
    from_user = message.from_user

    # ===== عرض الرتب =====
    if text == "رتب":
        msg = "🏷️ قائمة رتب البوت:\n\n"
        for i in range(1, MAX_RANK+1):
            name, price = RANKS[i]
            if price is None:
                msg += f"{i}. {name} — ❌ خاصة\n"
            else:
                msg += f"{i}. {name} — 💰 {price}\n"
        await bot.send_message(chat_id, msg)
        return

    # ===== عرض رتبتك =====
    if text == "رتبتي":
        rank = get_user_rank(uid) or 0
        name, _ = RANKS.get(rank, ["بدون رتبة", 0])
        await bot.send_message(chat_id, f"🎖️ رتبتك الحالية:\n{name} (# {rank})")
        return

    # ===== شراء رتبة =====
    if text.startswith("رتبة"):
        parts = text.split()
        if len(parts) != 2:
            await bot.send_message(chat_id, "❌ اكتب: رتبة <رقم>")
            return

        target_rank = int(parts[1])
        if target_rank > MAX_RANK or target_rank < 1:
            await bot.send_message(chat_id, "❌ رتبة غير موجودة")
            return

        # التحقق من المميز
        if uid not in SPECIAL_USERS and target_rank > 6:
            await bot.send_message(chat_id, "⚠️ لازم تكون مميز حتى تشتري رتب عالية")
            return

        current = get_user_rank(uid) or 0
        if target_rank != current + 1:
            await bot.send_message(chat_id, "❌ لازم تشتري الرتب بالترتيب")
            return

        name, price = RANKS[target_rank]
        if price is None:
            await bot.send_message(chat_id, "🚫 هذه الرتبة خاصة بالمشرف")
            return

        gold = get_user_gold(uid)
        if gold < price:
            await bot.send_message(chat_id, "💸 ذهبك غير كافي")
            return

        update_user_gold(uid, -price)
        set_user_rank(uid, target_rank)
        await bot.send_message(chat_id, f"✅ تمت الترقية!\n🎖️ رتبتك الجديدة: {name}")
        return

    # ===== رفع/تنزيل رتبة (للمالك فقط) =====
    if is_group:
        chat_member = await bot.get_chat_member(chat_id, uid)
        owner_id = None
        # العثور على المالك
        async for m in bot.get_chat_administrators(chat_id):
            if m.status == "creator":
                owner_id = m.user.id
                break

        if owner_id and uid == owner_id:
            # رفع رتبة بالقوة
            if text.startswith("ترقية"):
                parts = text.split()
                if len(parts) != 3:
                    await bot.send_message(chat_id, "❌ الصيغة: ترقية <UID> <رتبة>")
                    return

                target_uid = int(parts[1])
                target_rank = int(parts[2])
                if target_rank not in RANKS:
                    await bot.send_message(chat_id, "❌ رتبة غير موجودة")
                    return

                set_user_rank(target_uid, target_rank)
                name, _ = RANKS[target_rank]
                await bot.send_message(chat_id, f"👑 تمت الترقية!\nالرتبة الجديدة: {name}")
                # أعلى رتبة => اعطاء مشرف
                if target_rank == MAX_RANK:
                    try:
                        await bot.promote_chat_member(
                            chat_id, target_uid,
                            can_manage_chat=True,
                            can_delete_messages=True,
                            can_invite_users=True,
                            can_pin_messages=True,
                            can_change_info=True,
                            can_restrict_members=True
                        )
                    except:
                        pass
                return

            # تنزيل رتبة بالقوة
            if text.startswith("تنزيل"):
                parts = text.split()
                if len(parts) != 2:
                    await bot.send_message(chat_id, "❌ الصيغة: تنزيل <UID>")
                    return
                target_uid = int(parts[1])
                set_user_rank(target_uid, 0)
                await bot.send_message(chat_id, f"✅ تم تنزيل رتبة الشخص")
                return

    # ===== أمر رفع مميز =====
    if text in ["م", "مميز"]:
        if not is_group:
            await bot.send_message(chat_id, "⚠️ هذا الأمر خاص بالمجموعات")
            return
        if chat_member.status != "creator":
            await bot.send_message(chat_id, "❌ فقط المالك يقدر يرفع المميزين")
            return
        if message.reply_to_message:
            target_uid = message.reply_to_message.from_user.id
            SPECIAL_USERS.add(target_uid)
            add_special_user(target_uid)
            await bot.send_message(chat_id, f"✨ تم رفع العضو مميز")
            return

    # ===== تاك كل المميزين =====
    if text == "تاك":
        if not SPECIAL_USERS:
            await bot.send_message(chat_id, "⚠️ ماكو مميزين")
            return
        mentions = []
        for uid_special in SPECIAL_USERS:
            mentions.append(f"<a href='tg://user?id={uid_special}'>🟢</a>")
        await bot.send_message(chat_id, "🔹 المميزين:\n" + " ".join(mentions), parse_mode="HTML")
        return
