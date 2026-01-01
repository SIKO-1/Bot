import random
from db_manager import get_user, update_user

def register_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text == "تخمين")
    def start_guess(m):
        uid = m.from_user.id
        user_data = get_user(uid)
        balance = user_data.get("balance", 0)

        # التأكد من أن لديه رصيد كافٍ للخسارة (50 نقطة على الأقل)
        if balance < 50:
            return bot.reply_to(m, f"❌ رصيدك {balance} نقطة فقط. لازم يكون عندك 50 نقطة على الأقل عشان تخمن!")

        # توليد الرقم السري من 1 إلى 20
        secret_number = random.randint(1, 20)
        
        msg = bot.reply_to(m, "🎯 **لعبة التخمين الملكية**\n\nلقد اخترت رقماً سرياً من **1 إلى 20**.. خمن ما هو؟\n\n⚠️ _ملاحظة: لو فزت تاخذ 200، ولو خسرت ينخصم منك 50!_")
        
        # ننتقل للخطوة التالية لفحص رقم المستخدم
        bot.register_next_step_handler(msg, lambda message: check_guess(message, secret_number, bot))

    def check_guess(m, secret_num, bot):
        uid = m.from_user.id
        user_data = get_user(uid)
        balance = user_data.get("balance", 0)

        try:
            user_guess = int(m.text)
        except (ValueError, TypeError):
            return bot.reply_to(m, "⚠️ لازم ترسل رقم فقط! ضاعت عليك المحاولة وخصمت منك 50 لعدم التركيز 🌚")

        if user_guess == secret_num:
            # حالة الفوز
            new_bal = balance + 200
            update_user(uid, "balance", new_bal)
            bot.reply_to(m, f"🎉 **أسطورة!** تخمينك صح الرقم كان {secret_num}.\n💰 ربحت 200 نقطة!\n✨ رصيدك الجديد: {new_bal}")
        else:
            # حالة الخسارة
            new_bal = max(0, balance - 50)
            update_user(uid, "balance", new_bal)
            bot.reply_to(m, f"💀 **خطأ!** أنا اخترت الرقم {secret_num} وأنت كتبت {user_guess}.\n💸 خسرت 50 نقطة..\n✨ رصيدك المتبقي: {new_bal}")
