import db_manager
from telebot import types

# الهوية الإمبراطورية العظمى
EMPEROR_ID = 5860391324

def register_handlers(bot):

    # 🛑 حارس البوابة (منع المحظورين من الكلام نهائياً)
    @bot.message_handler(func=lambda m: db_manager.get_user(m.from_user.id).get("banned") == True)
    def gatekeeper(m):
        return

    # 💀 أمر الحظر (بالرد أو بالآيدي)
    @bot.message_handler(func=lambda m: m.text and m.text.startswith("حظر"))
    def ban_command(m):
        if m.from_user.id != EMPEROR_ID:
            return bot.reply_to(m, "⚠️ ويحك! أتظن أنك تملك مفاتيح السجن؟")

        target_id = None
        
        # الحالة 1: الحظر بالرد
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
        # الحالة 2: الحظر بالآيدي (مثال: حظر 123456)
        else:
            parts = m.text.split()
            if len(parts) > 1 and parts[1].isdigit():
                target_id = int(parts[1])

        if not target_id:
            return bot.reply_to(m, "👑 يا مولاي.. أشر بالرد على العبد أو اكتب الآيدي الخاص به بعد كلمة حظر.")

        db_manager.update_user(target_id, {"banned": True})
        try:
            bot.ban_chat_member(m.chat.id, target_id)
        except:
            pass
        
        bot.reply_to(m, f"💀 **مـرسـوم نـفـي**\nتم طرد العبد ذو الهوية ({target_id}) من ديارنا وإغلاق الأبواب في وجهه.")

    # ✨ أمر إلغاء الحظر (بالرد أو بالآيدي)
    @bot.message_handler(func=lambda m: m.text and m.text.startswith("عفو"))
    def unban_command(m):
        if m.from_user.id != EMPEROR_ID: return

        target_id = None
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
        else:
            parts = m.text.split()
            if len(parts) > 2 and parts[2].isdigit(): # لأن النص "الغاء الحظر 123"
                target_id = int(parts[2])

        if not target_id:
            return bot.reply_to(m, "👑 يا مولاي.. أشر بالرد أو اكتب الآيدي لإصدار العفو.")

        db_manager.update_user(target_id, {"banned": False})
        try:
            bot.unban_chat_member(m.chat.id, target_id)
        except:
            pass
        
        bot.reply_to(m, f"✨ **مـكـرمـة مـلـكـيـة**\nأُعيد العبد ({target_id}) إلى كنف الدولة بعد شموله بالعفو.")

    # 📜 سـجـل الـحـظر (قائمة المنفيين)
    @bot.message_handler(func=lambda m: m.text == "سجل الحظر")
    def ban_list(m):
        if m.from_user.id != EMPEROR_ID: return

        db = db_manager.load_db()
        banned_list = [uid for uid, data in db.items() if data.get("banned") == True]

        if not banned_list:
            return bot.reply_to(m, "سِجِلُّ الـنـفـي خـالٍ مـن الأرواح حـالـيـاً.")

        report = "📜 **قـائـمـة الـمـنـفـيـيـن مـن الإمـبـراطـوريـة :**\n"
        report += "----------------------------------\n"
        for i, uid in enumerate(banned_list, 1):
            report += f"{i} - الهوية: `{uid}`\n"
        report += "----------------------------------\n"
        report += "كـل مـن في هـذه الـقـائـمـة لا قـيـمـة لـهم."
        
        bot.reply_to(m, report)
