import random
from db_manager import get_user, update_user

def register_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text == "نرد")
    def dice_game(m):
        uid = m.from_user.id
        user_data = get_user(uid)
        balance = user_data.get("balance", 0)

        # إرسال النرد المتحرك
        dice_msg = bot.send_dice(m.chat.id)
        value = dice_msg.dice.value # قيمة النرد من 1 إلى 6

        # تحديد النتيجة بناءً على الرقم
        if value >= 5:
            # فوز كبير (رقم 5 أو 6)
            prize = 200
            new_bal = balance + prize
            update_user(uid, "balance", new_bal)
            bot.reply_to(m, f"🔥 **يا حظك!** طلعت لك {value}\n💰 ربحت الجائزة الكبرى: {prize} نقطة!\n✨ رصيدك الآن: {new_bal}")
            
        elif value >= 3:
            # فوز متوسط (رقم 3 أو 4)
            prize = 50
            new_bal = balance + prize
            update_user(uid, "balance", new_bal)
            bot.reply_to(m, f"🎲 حظ جيد، طلعت لك {value}\n💰 ربحت: {prize} نقطة.\n✨ رصيدك الآن: {new_bal}")
            
        else:
            # خسارة (رقم 1 أو 2)
            penalty = 30
            # التأكد إن الرصيد ما يصير بالسالب
            if balance < penalty:
                new_bal = 0
            else:
                new_bal = balance - penalty
                
            update_user(uid, "balance", new_bal)
            bot.reply_to(m, f"💀 **حظك سيء!** طلعت لك {value}\n💸 خسرنا منك {penalty} نقطة كضريبة للحظ..\n✨ رصيدك المتبقي: {new_bal}")

