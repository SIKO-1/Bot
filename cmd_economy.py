import db_manager
from telebot import types

# هويتك الإمبراطورية الفريدة
EMPEROR_ID = 5860391324

def register_handlers(bot):

    # 💰 1. أمر شحن رصيد (مثال: شحن 5000)
    @bot.message_handler(func=lambda m: m.text and m.text.startswith("شحن ") and m.from_user.id == EMPEROR_ID)
    def recharge_gold(m):
        if not m.reply_to_message:
            return bot.reply_to(m, "👑 يا إمبراطور، يجب الرد على رسالة الشخص لشحن رصيده.")

        try:
            # استخراج المبلغ من النص (بعد كلمة شحن)
            amount = int(m.text.split()[1])
            target_id = m.reply_to_message.from_user.id
            target_name = m.reply_to_message.from_user.first_name

            # تحديث الذهب في الخزنة
            db_manager.update_user_gold(target_id, amount)
            
            bot.reply_to(m, f"✅ **كرَم إمبراطوري!**\n\nتم شحن {amount} ذهبة للحساب: {target_name}\nاستمتع بها في خدمة الإمبراطورية.")
        except (IndexError, ValueError):
            bot.reply_to(m, "⚠️ خطأ في التنسيق! اكتب: شحن [المبلغ] بالرد على الشخص.")

    # 🧹 2. أمر تصفير رصيد شخص
    @bot.message_handler(func=lambda m: m.text == "تصفير رصيد" and m.from_user.id == EMPEROR_ID)
    def reset_gold(m):
        if not m.reply_to_message:
            return bot.reply_to(m, "👑 يا إمبراطور، تصفير الخزينة يتطلب الرد على رسالة العبد المعني.")

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        # جلب الرصيد الحالي لخصمه بالكامل وجعل النتيجة صفر
        current_bal = db_manager.get_user_gold(target_id)
        db_manager.update_user_gold(target_id, -current_bal)

        bot.reply_to(m, f"🧹 **تطهير مالي!**\n\nتم تصفير رصيد {target_name} بالكامل.\nعاد الآن فقيراً كما ولدته أمه.")

    # ⚠️ ردع المتطفلين الذين يحاولون استخدام أوامرك
    @bot.message_handler(func=lambda m: m.text and (m.text.startswith("شحن ") or m.text == "تصفير رصيد") and m.from_user.id != EMPEROR_ID)
    def stop_slaves_economy(m):
        bot.reply_to(m, "⚠️ أنت عبد من عباد الإمبراطور، لا تتجرأ على المساس بالخزنة الملكية!")

