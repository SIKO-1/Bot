# cmd_mute_kick.py
from db_manager import mute_user, unmute_user, get_muted_users, is_user_muted
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters

# المطورين
DEV_IDS = [5860391324, 7076215547, 7855813063]

COMMANDS_MUTE = ["كتم"]
COMMANDS_UNMUTE = ["رفع كتم"]
COMMANDS_LIST = ["قائمة المكتومين"]
COMMANDS_KICK = ["طرد"]

def handle(update: Update, context: CallbackContext):
    message = update.message
    if not message:
        return

    uid = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip() if message.text else ""

    # ===== التحقق من صلاحية المشرف/المالك/المطور =====
    member = message.chat.get_member(uid)
    is_admin = member.status in ['administrator', 'creator'] or uid in DEV_IDS

    # ===== كتم المستخدم =====
    if any(text.startswith(cmd) for cmd in COMMANDS_MUTE):
        if not is_admin:
            message.reply_text("❌ فقط المالك أو المشرف يمكنه استخدام هذا الأمر!")
            return
        if not message.reply_to_message:
            message.reply_text("⚠️ الرجاء الرد على رسالة الشخص الذي تريد كتمه!")
            return
        target_id = message.reply_to_message.from_user.id
        mute_user(chat_id, target_id)  # حفظ الكتم في قاعدة بيانات لكل مجموعة
        message.reply_text(f"🔇 تم كتم الشخص بنجاح!")

    # ===== رفع الكتم =====
    if any(text.startswith(cmd) for cmd in COMMANDS_UNMUTE):
        if not is_admin:
            message.reply_text("❌ فقط المالك أو المشرف يمكنه استخدام هذا الأمر!")
            return
        if not message.reply_to_message:
            message.reply_text("⚠️ الرجاء الرد على رسالة الشخص الذي تريد رفع كتمه!")
            return
        target_id = message.reply_to_message.from_user.id
        unmute_user(chat_id, target_id)
        message.reply_text(f"🔊 تم رفع الكتم عن الشخص!")

    # ===== قائمة المكتومين =====
    if text in COMMANDS_LIST:
        if not is_admin:
            message.reply_text("❌ فقط المالك أو المشرف يمكنه استخدام هذا الأمر!")
            return
        muted = get_muted_users(chat_id) or []
        if not muted:
            message.reply_text("📜 لا يوجد أي شخص مكتوم حالياً في هذه المجموعة.")
            return
        msg_text = "📜 قائمة المكتومين:\n\n"
        for u in muted:
            msg_text += f"👤 ID: {u}\n"
        message.reply_text(msg_text)

    # ===== طرد المستخدم =====
    if any(text.startswith(cmd) for cmd in COMMANDS_KICK):
        if not is_admin:
            message.reply_text("❌ فقط المالك أو المشرف يمكنه استخدام هذا الأمر!")
            return
        if not message.reply_to_message:
            message.reply_text("⚠️ الرجاء الرد على رسالة الشخص الذي تريد طرده!")
            return
        target_id = message.reply_to_message.from_user.id
        try:
            context.bot.kick_chat_member(chat_id, target_id)
            message.reply_text(f"👢 تم طرد الشخص من المجموعة!")
        except Exception as e:
            message.reply_text(f"❌ حدث خطأ أثناء الطرد: {e}")

    # ===== منع المكتومين من إرسال رسائل =====
    if is_user_muted(chat_id, uid):
        try:
            message.delete()
        except Exception:
            pass
