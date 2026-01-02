import random
from telebot import types

# نظام النقاط المرتبط بالـ Volume
try:
    from db_manager import get_user, update_user
except:
    def get_user(uid): return {"balance": 1000}
    def update_user(uid, k, v): pass

def register_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text == "تخمين")
    def start_guess(m):
        uid = m.from_user.id
        user_bal = get_user(uid).get("balance", 0)

        # التأكد من هيبة الرصيد
        if user_bal < 50:
            return bot.reply_to(m, f"❌ رصيدك {user_bal} نقطة فقط. القوانين الصارمة تمنع دخولك التحدي بأقل من 50 نقطة!")

        # توليد الرقم السري (نطاق أوسع لزيادة التحدي)
        secret_number = random.randint(1, 15)
        
        text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ تـحـدي الـتـخـمـيـن ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            "🎯 لقد اخترت رقماً سرياً من [ 1 إلى 15 ]\n"
            "🧠 استخدم حدسك الإمبراطوري وخمن الرقم؟\n\n"
            "💰 الـفـوز : +200 نـقـطـة\n"
            "💸 الـخـسارة : -50 نـقـطـة"
        )
        
        msg = bot.send_message(m.chat.id, text)
        # الانتظار للرد التالي من نفس المستخدم
        bot.register_next_step_handler(msg, lambda message: check_guess(message, secret_number, bot))

    def check_guess(m, secret_num, bot):
        uid = m.from_user.id
        user_bal = get_user(uid).get("balance", 0)

        # التأكد أن المدخل رقم
        try:
            user_guess = int(m.text)
        except:
            update_user(uid, "balance", max(0, user_bal - 50))
            return bot.reply_to(m, "⚠️ أرسلت نصاً وليس رقماً! تم خصم 50 نقطة كغرامة لعدم التركيز 🌚")

        if user_guess == secret_num:
            # حالة الانتصار العظيم
            update_user(uid, "balance", user_bal + 200)
            win_text = (
                "⌯ انـتـصـار إمـبـراطـوري ⌯\n"
                "━━━━━━━━━━━━━━\n"
                f"👤 الـبـطل : {m.from_user.first_name}\n"
                f"✅ الـتـخـمـين : {user_guess} (صح)\n"
                "💰 الـجـوائـز : +200 نـقـطـة"
            )
            bot.reply_to(m, win_text)
        else:
            # حالة الخيبة
            update_user(uid, "balance", max(0, user_bal - 50))
            fail_text = (
                "⌯ خـيـبـة أمـل ⌯\n"
                "━━━━━━━━━━━━━━\n"
                f"❌ تخمينك كان : {user_guess}\n"
                f"💡 الرقم الصحيح : {secret_num}\n"
                "💸 الخسارة : -50 نقطة"
            )
            bot.reply_to(m, fail_text)
