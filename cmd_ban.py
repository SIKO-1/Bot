import db_manager
from telebot import types

# هويتك الإمبراطورية العظمى
EMPEROR_ID = 5860391324

def register_handlers(bot):

    # دالة التحقق من السلطة
    def is_authorized(user_id):
        if user_id == EMPEROR_ID: return True
        user_data = db_manager.get_user(user_id)
        return user_data.get("rank") == "admin"

    # 🛑 أهم دالة: منع المحظورين من استخدام البوت
    @bot.message_handler(func=lambda m: db_manager.get_user(m.from_user.id).get("banned") == True, priority=1)
    def block_access(m):
        # البوت هنا يلتزم الصمت التام ولا يرد على المحظور
        return

    # 💀 أمر الحظر الشامل (بالرد)
    @bot.message_handler(func=lambda m: m.text == "حظر")
    def ban_from_bot(m):
        if not is_authorized(m.from_user.id):
            bot.reply_to(m, "⚠️ **وَيْحَكَ!** أتظن أنك تملك مفاتيح السجن؟ اِلزم مكانك أيها العبد!")
            return

        if not m.reply_to_message:
            return bot.reply_to(m, "👑 **يا جلالة الإمبراطور..** أشر بيمينك (بالرد) على من تريد إقصاءه من رحابنا.")

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        # تحديث حالته في الخزنة كـ "محظور"
        db_manager.update_user(target_id, {"banned": True})
        
        bot.reply_to(m, f"💀 **مـرسـوم الإقـصـاء**\n\nلقد أُغلق باب الإمبراطورية في وجه {target_name}! لن يسمع منه البوت ولن يجيبه، وقد نُبذ وراء الأسوار.")

    # ✨ أمر العفو الشامل (بالرد)
    @bot.message_handler(func=lambda m: m.text == "الغاء الحظر")
    def unban_from_bot(m):
        if not is_authorized(m.from_user.id):
            return bot.reply_to(m, "⚠️ **توقف!** مفاتيح القيود ليست بيد من هب ودب، بل بيد الأسياد.")

        if not m.reply_to_message:
            return bot.reply_to(m, "👑 **يا سيدي الإمبراطور..** من هو العبد الذي نال عفوك الكريم؟ رد على رسالته.")

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        # فتح الأبواب له مجدداً
        db_manager.update_user(target_id, {"banned": False})
        
        bot.reply_to(m, f"✨ **مـكـرمـة مـلـكـيـة**\n\nلقد رُفع الحظر عن {target_name} بفضل جود الإمبراطور. عُد لخدمتنا ولا تكن من الجاهلين.")
