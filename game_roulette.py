import random
import time
from db_manager import get_user, update_user

def register_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text.startswith("روليت"))
    def roulette_game(m):
        uid = m.from_user.id
        user_data = get_user(uid)
        balance = user_data.get("balance", 0)

        # 1. التأكد من كتابة المبلغ
        parts = m.text.split()
        if len(parts) < 2:
            return bot.reply_to(m, "⚠️ يجب كتابة مبلغ للرهان! مثال: `روليت 100`")
        
        try:
            bet = int(parts[1])
        except ValueError:
            return bot.reply_to(m, "❌ يرجى كتابة أرقام فقط!")

        # 2. التأكد من توفر الرصيد
        if bet <= 0:
            return bot.reply_to(m, "🚫 لا يمكنك الرهان بمبلغ صفر أو سالب!")
        
        if bet > balance:
            return bot.reply_to(m, f"💸 رصيدك الحالي {balance} نقطة فقط، لا يمكنك الرهان بـ {bet}!")

        # 3. بدء اللعب (التشويق)
        status_msg = bot.reply_to(m, "🎰 جاري تدوير عجلة الروليت... استعد! 🌀")
        time.sleep(2) # انتظار لمدة ثانيتين للحماس

        # 4. تحديد النتيجة
        win = random.choice([True, False])

        if win:
            new_bal = balance + bet # إضافة الربح (الضعف)
            update_user(uid, "balance", new_bal)
            bot.edit_message_text(f"🔥 **كفووو! الروليت توقفت على اللون الأخضر!**\n💰 ربحت: {bet} نقطة إضافية.\n✨ رصيدك الآن: {new_bal}", 
                                  chat_id=m.chat.id, message_id=status_msg.message_id)
        else:
            new_bal = balance - bet # سحب الخسارة
            update_user(uid, "balance", new_bal)
            bot.edit_message_text(f"💀 **للأسف! الروليت توقفت على اللون الأحمر..**\n💸 خسرت: {bet} نقطة.\n✨ رصيدك المتبقي: {new_bal}", 
                                  chat_id=m.chat.id, message_id=status_msg.message_id)
