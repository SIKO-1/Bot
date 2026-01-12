from aiogram import types
from db_manager import (
    _get_user, get_all_users_count, update_user_gold, get_group_users
)

# ======================
# إعداد المطورين
# ======================
DEV_IDS = [5860391324, 7855813063, 7076215547]

# أوامر
COMMANDS = ["احصائيات", "سحب", "تصنيف"]

# ======================
# التعامل مع الرسائل
# ======================
async def handle(bot, message: types.Message):
    text = message.text.strip()
    uid = message.from_user.id
    chat_id = message.chat.id
    is_group = message.chat.type in ["group", "supergroup"]

    # ماكو أمر من أوامرنا
    if not any(text.startswith(cmd) for cmd in COMMANDS):
        return

    # ======================
    # احصائيات المستخدم العادية
    # ======================
    if text.startswith("احصائيات"):
        if not is_group:
            user = await _get_user(uid)
            gold = user.gold or 0
            bank = user.bank or 0
            msgs = user.total_messages or 0
            daily = user.daily_usage or 0
            banned = "✅" if not user.banned else "❌"

            name_display = user.name or str(uid)
            report = f"""
╔═════════════════╗
أهلاً بك في إدارة المستخدمين
╚═════════════════╝

عدد المستخدمين الكلي: {await get_all_users_count()}

━━━━━━━━━━━━━━━
معلوماتك:
• الاسم: {name_display}
• الذهب: {gold}
• البنك: {bank}
• عدد الرسائل الكلي: {msgs}
• الاستخدام اليومي: {daily}
• محظور: {banned}
━━━━━━━━━━━━━━━
"""
            await bot.send_message(chat_id, report)
            return

        # ======================
        # احصائيات المجموعة
        # ======================
        group_users = await get_group_users(chat_id)
        if not group_users:
            await bot.send_message(chat_id, "⚠️ لا يوجد بيانات للمجموعة")
            return

        # ترتيب حسب عدد الرسائل
        sorted_msgs = sorted(group_users, key=lambda x: x.total_messages, reverse=True)
        sorted_gold = sorted(group_users, key=lambda x: x.gold, reverse=True)

        top_msgs = "\n".join([f"{u.name}: {u.total_messages} رسالة" for u in sorted_msgs[:10]])
        top_gold = "\n".join([f"{u.name}: {u.gold} ذهب" for u in sorted_gold[:10]])

        report = f"""
📊 احصائيات المجموعة:

🏆 الأكثر نشاطاً:
{top_msgs}

💰 الأغنى:
{top_gold}

عدد الأعضاء الكلي: {len(group_users)}
"""
        await bot.send_message(chat_id, report)
        return

    # ======================
    # سحب الذهب (للمطورين فقط)
    # ======================
    if text.startswith("سحب"):
        if uid not in DEV_IDS:
            await bot.send_message(chat_id, "❌ هذا الأمر للمطور فقط")
            return

        parts = text.split()
        if len(parts) != 3:
            await bot.send_message(chat_id, "❌ صيغة الأمر: سحب <UID> <المبلغ>")
            return

        target_uid = int(parts[1])
        amount = int(parts[2])

        await update_user_gold(target_uid, -amount)
        await bot.send_message(chat_id, f"✅ تم سحب {amount} ذهب من المستخدم {target_uid}")
        return

    # ======================
    # تصنيف / إعطاء صلاحيات للمشرفين
    # ======================
    if text.startswith("تصنيف"):
        if not is_group:
            await bot.send_message(chat_id, "⚠️ هذا الأمر خاص بالمجموعات فقط")
            return

        chat_member = await bot.get_chat_member(chat_id, uid)
        if chat_member.status not in ["administrator", "creator"]:
            await bot.send_message(chat_id, "❌ فقط المشرفين أو المالك يمكنهم استخدام هذا الأمر")
            return

        # أمثلة على التصنيف
        group_users = await get_group_users(chat_id)
        sorted_msgs = sorted(group_users, key=lambda x: x.total_messages, reverse=True)
        mentions = "\n".join([f"{u.name}: {u.total_messages} رسالة" for u in sorted_msgs[:10]])
        await bot.send_message(chat_id, f"📊 تصنيف الأعضاء حسب الرسائل:\n{mentions}")
        return
