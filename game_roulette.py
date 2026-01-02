import random
import time
from telebot import types

# نظام النقاط المرتبط بالـ Volume
try:
    from db_manager import get_user, update_user
except:
    def get_user(uid): return {"balance": 0}
    def update_user(uid, k, v): pass

def register_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text.startswith("روليت"))
    def roulette_game(m):
        uid = m.from_user.id
        user_data = get_user(uid)
        balance = user_data.get("balance", 0)

        # 1. التأكد من كتابة المبلغ
        parts = m.text.split()
        if len(parts) < 2:
            text_err = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ تـنـبـيـه مـلـكـي ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                "⚠️ يجب كتابة مبلغ للرهان!\n"
                "💡 مـثـال : روليت 100"
            )
            return bot.reply_to(m, text_err)
        
        try:
            bet = int(parts[1])
        except ValueError:
            return bot.reply_to(m, "❌ عذراً.. يرجى كتابة أرقام فقط!")

        # 2. التأكد من توفر الرصيد والشروط
        if bet <= 0:
            return bot.reply_to(m, "🚫 لا يمكن المراهنة بمبلغ وهمي!")
        
        if bet > balance:
            text_poor = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ عـجـز مـالـي ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"💸 رصيدك الحالي {balance} نقطة فقط\n"
                f"❌ لا يمكنك الرهان بمبلغ {bet}"
            )
            return bot.reply_to(m, text_poor)

        # 3. واجهة تدوير العجلة (التشويق)
        text_start = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ رولـيـت مـلـكـي ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"💰 المراهنة على : [ {bet} ] نقطة\n"
            "🌀 جـاري تـدويـر الـعـجـلـة..."
        )
        status_msg = bot.reply_to(m, text_start)
        
        # حركة تشويقية (تعديل الرسالة)
        time.sleep(1.5)
        bot.edit_message_text(f"{text_start}\n\n⚡️ العجلة بدأت تتباطأ...", chat_id=m.chat.id, message_id=status_msg.message_id)
        time.sleep(1.5)

        # 4. تحديد النتيجة (حظ الإمبراطور)
        win = random.choice([True, False])

        if win:
            new_bal = balance + bet
            update_user(uid, "balance", new_bal)
            win_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ نـتـيـجـة الـفـوز ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"👤 الإمبراطور : {m.from_user.first_name}\n"
                "🟢 النتيجة : فوز ساحق!\n"
                f"💰 الأرباح : +{bet} نقطة\n"
                f"✨ الرصيد الحالي : {new_bal}"
            )
            bot.edit_message_text(win_text, chat_id=m.chat.id, message_id=status_msg.message_id)
        else:
            new_bal = balance - bet
            update_user(uid, "balance", new_bal)
            fail_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ نـتـيـجـة الـخـسـارة ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"👤 الإمبراطور : {m.from_user.first_name}\n"
                "🔴 النتيجة : حظ سيء!\n"
                f"💸 الخسارة : -{bet} نقطة\n"
                f"✨ الرصيد المتبقي : {new_bal}"
            )
            bot.edit_message_text(fail_text, chat_id=m.chat.id, message_id=status_msg.message_id)
