import random
import time
import db_manager  # الربط مع الخزنة الحديدية

def handle(bot, message):
    if not message.text.startswith("روليت"):
        return

    uid = message.from_user.id
    user_gold = db_manager.get_user_gold(uid)

    # 1. التأكد من كتابة مبلغ الرهان
    parts = message.text.split()
    if len(parts) < 2:
        text_err = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ تنبيه ملكي ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            "⚠️ يجب تحديد مبلغ الرهان من خزنتك!\n"
            "💡 مثال : روليت 500"
        )
        return bot.reply_to(message, text_err)

    try:
        bet = int(parts[1])
    except ValueError:
        return bot.reply_to(message, "❌ يا ملك.. يرجى كتابة الرهان بالأرقام فقط!")

    # 2. قوانين الإمبراطورية للرهان
    if bet <= 0:
        return bot.reply_to(message, "🚫 لا يمكنك الرهان بالهواء! ضع ذهباً حقيقياً.")

    if bet > user_gold:
        text_poor = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ عجز مالي ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"💸 رصيدك الحالي: {user_gold} ذهبة فقط\n"
            f"❌ لا يمكنك الرهان بمبلغ {bet}.. العب بذكاء!"
        )
        return bot.reply_to(message, text_poor)

    # 3. واجهة تدوير العجلة
    text_start = (
        "┏━━━━━━━ ● ━━━━━━━┓\n"
        "         ⌯ روليت ملكي ⌯\n"
        "┗━━━━━━━ ● ━━━━━━━┛\n\n"
        f"💰 الرهان على : [ {bet} ] ذهبة\n"
        "🌀 جاري تدوير عجلة القدر..."
    )
    status_msg = bot.reply_to(message, text_start)

    # 4. تشويق تدريجي
    time.sleep(1.5)
    bot.edit_message_text(f"{text_start}\n\n⚡️ العجلة بدأت تتباطأ وتتوقف...", chat_id=message.chat.id, message_id=status_msg.message_id)
    time.sleep(1.5)

    # 5. تحديد النتيجة
    outcome = random.choices(
        ["win", "lose", "jackpot"], 
        weights=[45, 50, 5],  # 5% فرصة جاكبوت، 45% فوز، 50% خسارة
        k=1
    )[0]

    if outcome == "win":
        db_manager.update_user_gold(uid, bet)
        new_bal = user_gold + bet
        result_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ فوز ساحق ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"👑 الإمبراطور : {message.from_user.first_name}\n"
            "🟢 النتيجة : فوز مبارك!\n"
            f"💰 الأرباح : +{bet} ذهبة\n"
            f"✨ رصيدك الآن : {new_bal} ذهبة"
        )

    elif outcome == "jackpot":
        jackpot = bet * 5
        db_manager.update_user_gold(uid, jackpot)
        new_bal = user_gold + jackpot
        result_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ جاكبوت الملك ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"👑 الإمبراطور : {message.from_user.first_name}\n"
            "💥 النتيجة : جاكبوت مذهل!\n"
            f"💰 الأرباح : +{jackpot} ذهبة\n"
            f"✨ رصيدك الآن : {new_bal} ذهبة"
        )
    else:
        db_manager.update_user_gold(uid, -bet)
        new_bal = user_gold - bet
        result_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ خسارة ساحقه ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"👑 الإمبراطور : {message.from_user.first_name}\n"
            "🔴 النتيجة : غدرت بك العجلة!\n"
            f"💸 الخسارة : -{bet} ذهبة\n"
            f"✨ المتبقي لك : {new_bal} ذهبة"
        )

    bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=status_msg.message_id)
