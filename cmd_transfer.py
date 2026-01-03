import db_manager
from telebot import types

def register_handlers(bot):

    # أمر التحويل (مثال: تحويل 500 بالرد على الشخص)
    @bot.message_handler(func=lambda m: m.text and m.text.startswith("تحويل "))
    def transfer_gold(m):
        sender_id = m.from_user.id
        sender_name = m.from_user.first_name
        
        # 1. التأكد من الرد على رسالة الشخص المستلم
        if not m.reply_to_message:
            return bot.reply_to(m, "⚠️ يجب أن ترد على رسالة الشخص الذي تريد التحويل إليه!")

        receiver_id = m.reply_to_message.from_user.id
        receiver_name = m.reply_to_message.from_user.first_name

        # 2. منع التحويل للنفس
        if sender_id == receiver_id:
            return bot.reply_to(m, "🤨 هل تحاول خداع الإمبراطورية؟ لا يمكنك التحويل لنفسك!")

        try:
            # 3. استخراج المبلغ
            amount = int(m.text.split()[1])
            
            if amount <= 0:
                return bot.reply_to(m, "⚠️ يجب أن يكون المبلغ أكبر من صفر!")

            # 4. التحقق من رصيد المرسل
            sender_bal = db_manager.get_user_gold(sender_id)
            
            if sender_bal < amount:
                return bot.reply_to(m, f"❌ رصيدك لا يكفي! تملك {sender_bal} ذهبة فقط.")

            # 5. تنفيذ العملية (خصم من المرسل وإضافة للمستلم)
            db_manager.update_user_gold(sender_id, -amount)
            db_manager.update_user_gold(receiver_id, amount)

            transfer_text = (
                "💸 **عـمـلـيـة تـحـويـل نـاجـحـة**\n"
                "━━━━━━━━━━━━━━\n"
                f"📤 مـن : {sender_name}\n"
                f"📥 إلـى : {receiver_name}\n"
                f"💰 الـمـبـلـغ : {amount} ذهـبـة\n\n"
                "🛡️ تمت العملية بمباركة الإمبراطورية."
            )
            bot.reply_to(m, transfer_text)

        except (IndexError, ValueError):
            bot.reply_to(m, "⚠️ استخدم الصيغة الصحيحة: (تحويل + المبلغ) بالرد على الشخص.")

