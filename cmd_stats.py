import telebot
import db_manager
import math

COMMANDS = ["إحصائيات", "سحب", "تصنيف"]

def handle(bot: telebot.TeleBot, message: telebot.types.Message):
    text = message.text or ""
    uid = message.from_user.id

    if not any(text.startswith(cmd) for cmd in COMMANDS):
        return

    # =========================
    # إحصائيات المستخدمين
    # =========================
    if text.startswith("إحصائيات"):
        all_users = db_manager.get_all_users()
        total_users = len(all_users)

        reply = "╔═════════════════╗\n"
        reply += f"  أهلاً بك يا {message.from_user.first_name} في إدارة المستخدمين\n"
        reply += "╚═════════════════╝\n\n"
        reply += f"عدد المستخدمين الكلي: {total_users}\n\n"

        banned = [u for u in all_users if u.get("banned", False)]
        not_banned = [u for u in all_users if not u.get("banned", False)]

        reply += "━━━━━━━━━━━━━━━\n"
        reply += "الاشخاص المحظورين:\n\n"
        for u in banned:
            name = u.get("name") or "غير معروف"
            username = f"@{u['username']}" if u.get("username") else "لا يوجد"
            reply += f"- {name} / {username} / ذهب: {u['gold']} / بنك: {u['bank']} ✅\n"

        reply += "━━━━━━━━━━━━━━━\n"
        reply += "الاشخاص غير محظورين:\n\n"
        for u in not_banned:
            name = u.get("name") or "غير معروف"
            username = f"@{u['username']}" if u.get("username") else "لا يوجد"
            reply += f"- {name} / {username} / ذهب: {u['gold']} / بنك: {u['bank']}\n"

        reply += "━━━━━━━━━━━━━━━"
        bot.reply_to(message, reply)

    # =========================
    # سحب الذهب من مستخدم
    # =========================
    elif text.startswith("سحب"):
        parts = text.split()
        if len(parts) < 3:
            bot.reply_to(message, "⚠️ مثال صحيح: سحب <UID> <المبلغ>")
            return

        target = parts[1]
        try:
            amount = int(parts[2])
        except:
            bot.reply_to(message, "❌ المبلغ يجب أن يكون رقم صحيح!")
            return

        # إذا الرد على رسالة شخص
        target_uid = None
        if message.reply_to_message:
            target_uid = message.reply_to_message.from_user.id
        else:
            # جرب تحويل النص لـ int UID
            try:
                target_uid = int(target)
            except:
                bot.reply_to(message, "❌ لم أستطع تحديد المستخدم، استخدم الـ UID أو الرد على رسالته")
                return

        if db_manager.sweep_gold(target_uid, amount):
            bot.reply_to(message, f"✅ تم سحب {amount} ذهب من المستخدم {target_uid}")
        else:
            bot.reply_to(message, f"⚠️ المستخدم {target_uid} لا يمتلك هذا المبلغ!")

    # =========================
    # قائمة التصنيف
    # =========================
    elif text.startswith("تصنيف"):
        richest = db_manager.get_richest(5)
        active = db_manager.get_most_active(5)

        reply = "╔═════════════════╗\n"
        reply += "   قائمة التصنيف\n"
        reply += "╚═════════════════╝\n\n"

        reply += "أغنى 5 أشخاص بالبوت:\n\n"
        for idx, u in enumerate(richest, 1):
            name = u.get("name") or "غير معروف"
            username = f"@{u['username']}" if u.get("username") else "لا يوجد"
            gold = u.get("gold", 0)
            reply += f"{idx}- {name} / {username} / ذهب: {gold}\n"

        reply += "\n━━━━━━━━━━━━━━\n"
        reply += "أكثر 5 أشخاص تفاعلاً:\n\n"
        for idx, u in enumerate(active, 1):
            name = u.get("name") or "غير معروف"
            username = f"@{u['username']}" if u.get("username") else "لا يوجد"
            usage = u.get("total_messages", 0)
            reply += f"{idx}- {name} / {username} / رسائل: {usage}\n"

        reply += "━━━━━━━━━━━━━━━"
        bot.reply_to(message, reply)
