import random
import time
import db_manager

COMMAND = "روليت"
MISSION_TYPE = "roulette"       # نوع المهمة للروليت في db_manager
REWARD_ITEM = "🎁 صندوق الحظ النادر"

def handle(bot, message):
    if not message.text.startswith(COMMAND):
        return

    uid = message.from_user.id
    user_gold = db_manager.get_user_gold(uid)

    # ───────── 1. التحقق من الرهان ─────────
    parts = message.text.split()
    if len(parts) < 2:
        return bot.reply_to(
            message,
            "⚠️ يجب تحديد مبلغ الرهان\n"
            "💡 مثال: روليت 500"
        )

    try:
        bet = int(parts[1])
    except ValueError:
        return bot.reply_to(message, "❌ الرهان يجب أن يكون رقماً صحيحاً")

    if bet <= 0:
        return bot.reply_to(message, "🚫 لا يمكنك الرهان بمبلغ صفر أو أقل")

    if bet > user_gold:
        return bot.reply_to(
            message,
            f"💸 رصيدك الحالي: {user_gold} ذهب\n"
            "❌ لا تملك ذهباً كافياً"
        )

    # ───────── 2. واجهة اللعب ─────────
    start_text = (
        "┏━━━━━━━ ● ━━━━━━━┓\n"
        "      🎰 روليت الإمبراطورية 🎰\n"
        "┗━━━━━━━ ● ━━━━━━━┛\n\n"
        f"💰 الرهان: {bet} ذهبة\n"
        "🌀 تدوير عجلة القدر..."
    )
    status_msg = bot.reply_to(message, start_text)
    time.sleep(1.5)
    bot.edit_message_text(
        start_text + "\n\n⚡️ العجلة تتباطأ...",
        chat_id=message.chat.id,
        message_id=status_msg.message_id
    )
    time.sleep(1.5)

    # ───────── 3. تحديد النتيجة ─────────
    outcome = random.choices(
        ["win", "lose", "jackpot"],
        weights=[45, 50, 5],
        k=1
    )[0]

    # ───────── 4. النتائج ─────────
    if outcome == "win":
        new_bal = db_manager.update_user_gold(uid, bet)
        result_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ فـوز إمـبـراطـوري ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🔥 الحظ يبتسم لك : [ الفوز ]\n"
            f"💰 الجائزة : +{bet} ذهب\n"
            f"✨ رصيدك الحالي : {new_bal} ذهب"
        )

    elif outcome == "jackpot":
        jackpot = bet * 5
        new_bal = db_manager.update_user_gold(uid, jackpot)
        result_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ جاكبوت أسطوري ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🔥 الحظ يبتسم لك : [ الجاكبوت ]\n"
            f"💰 الجائزة : +{jackpot} ذهب\n"
            f"✨ رصيدك الحالي : {new_bal} ذهب"
        )

    else:
        new_bal = db_manager.update_user_gold(uid, -bet)
        result_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ خسارة ساحقة ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"💀 الحظ : [ الخسارة ]\n"
            f"💸 خسارتك : -{bet} ذهب\n"
            f"✨ رصيدك الحالي : {new_bal} ذهب"
        )

    bot.edit_message_text(
        result_text,
        chat_id=message.chat.id,
        message_id=status_msg.message_id
    )

    # ───────── 5. التحقق من المهمة اليومية ─────────
    mission_completed = db_manager.complete_mission(uid, MISSION_TYPE)
    if mission_completed:
        db_manager.add_to_inventory(uid, REWARD_ITEM)
        bot.send_message(
            message.chat.id,
            "✅ تم إكمال المهمة اليومية!\n"
            f"🎁 تم إضافة {REWARD_ITEM} إلى مخزونك"
        )
