import db_manager
from telebot import types

# هويتك الإمبراطورية
EMPEROR_ID = 5860391324

def register_handlers(bot):

    # دالة التحقق من السلطة (الإمبراطور أو الأدمن)
    def is_authorized(user_id):
        if user_id == EMPEROR_ID:
            return True
        user_data = db_manager.get_user(user_id)
        return user_data.get("rank") == "admin"

    # 🚫 أمر حظر (بالرد على الشخص)
    @bot.message_handler(func=lambda m: m.text == "حظر")
    def ban_user(m):
        if not is_authorized(m.from_user.id):
            bot.reply_to(m, "⚠️ لا يملك العبيد سلطة الحظر والتشريد!")
            return

        if not m.reply_to_message:
            return bot.reply_to(m, "👑 يا سيدي، الحظر يتطلب تحديد الضحية بالرد على رسالته.")

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        try:
            # تسجيل الحظر في قاعدة البيانات (منعه من استخدام أوامر البوت)
            db_manager.update_user(target_id, {"banned": True})
            
            # طرده فعلياً من المجموعة (اختياري)
            bot.ban_chat_member(m.chat.id, target_id)
            
            bot.reply_to(m, f"💀 **نـفـي أبـدي!**\n\nتم حظر {target_name} من الإمبراطورية وطرده.\nلن يجرؤ على العودة مجدداً.")
        except Exception as e:
            bot.reply_to(m, f"⚠️ حدث خطأ أثناء تنفيذ النفي: {e}")

    # ♻️ أمر الغاء الحظر (بالرد أو عبر الـ ID)
    @bot.message_handler(func=lambda m: m.text == "الغاء الحظر")
    def unban_user(m):
        if not is_authorized(m.from_user.id):
            return bot.reply_to(m, "⚠️ عفو الإمبراطور لا يصدره إلا أهله!")

        if not m.reply_to_message:
            return bot.reply_to(m, "👑 يا سيدي، الرد مطلوب لفك الحظر.")

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        try:
            # إزالة الحظر من قاعدة البيانات
            db_manager.update_user(target_id, {"banned": False})
            
            # السماح له بدخول المجموعة مجدداً
            bot.unban_chat_member(m.chat.id, target_id)
            
            bot.reply_to(m, f"✨ **عـفـو مـلـكـي!**\n\nتم إلغاء حظر {target_name}.\nأُعطي فرصة ثانية للحياة تحت رايتنا.")
        except Exception as e:
            bot.reply_to(m, f"⚠️ خطأ في العفو: {e}")
