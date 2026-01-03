import random
import time
import db_manager # الربط مع الخزنة الحديدية

def register_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text.startswith("روليت"))
    def roulette_game(m):
        uid = m.from_user.id
        # جلب الذهب الحقيقي من النظام
        user_gold = db_manager.get_user_gold(uid)

        # 1. التأكد من كتابة مبلغ الرهان
        parts = m.text.split()
        if len(parts) < 2:
            text_err = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ تـنـبـيـه مـلـكـي ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                "⚠️ يجب تحديد مبلغ للرهان من خزنتك!\n"
                "💡 مـثـال : روليت 500"
            )
            return bot.reply_to(m, text_err)
        
        try:
            bet = int(parts[1])
        except ValueError:
            return bot.reply_to(m, "❌ يا ملك.. يرجى كتابة الرهان بالأرقام فقط!")

        # 2. قوانين الإمبراطورية للرهان
        if bet <= 0:
            return bot.reply_to(m, "🚫 لا يمكنك الرهان بالهواء! ضع ذهباً حقيقياً.")
        
        if bet > user_gold:
            text_poor = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ عـجـز مـالـي ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"💸 رصيدك الحالي {user_gold} ذهبة فقط\n"
                f"❌ لا يمكنك الرهان بمبلغ {bet}.. العب بذكاء!"
            )
            return bot.reply_to(m, text_poor)

        # 3. واجهة تدوير العجلة (التشويق الملكي)
        text_start = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ رولـيـت مـلـكـي ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"💰 الرهان على : [ {bet} ] ذهبة\n"
            "🌀 جـاري تـدويـر عـجـلـة الـقـدر..."
        )
        status_msg = bot.reply_to(m, text_start)
        
        time.sleep(1.5)
        bot.edit_message_text(f"{text_start}\n\n⚡️ العجلة بدأت تتباطأ وتتوقف...", chat_id=m.chat.id, message_id=status_msg.message_id)
        time.sleep(1.5)

        # 4. النتيجة النهائية
        win = random.choice([True, False])

        if win:
            # إضافة الذهب للخزنة
            db_manager.update_user_gold(uid, bet)
            new_bal = user_gold + bet
            win_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ نـتـيـجـة الـفـوز ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"👤 الإمبراطور : {m.from_user.first_name}\n"
                "🟢 النتيجة : فوز ساحق ومبارك!\n"
                f"💰 الأرباح : +{bet} ذهبة\n"
                f"✨ رصيدك الآن : {new_bal} ذهبة"
            )
            bot.edit_message_text(win_text, chat_id=m.chat.id, message_id=status_msg.message_id)
        else:
            # خصم الذهب من الخزنة
            db_manager.update_user_gold(uid, -bet)
            new_bal = user_gold - bet
            fail_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ نـتـيـجـة الـخـسـارة ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"👤 الإمبراطور : {m.from_user.first_name}\n"
                "🔴 النتيجة : غدرت بك العجلة!\n"
                f"💸 الخسارة : -{bet} ذهبة\n"
                f"✨ المتبقي لك : {new_bal} ذهبة"
            )
            bot.edit_message_text(fail_text, chat_id=m.chat.id, message_id=status_msg.message_id)
