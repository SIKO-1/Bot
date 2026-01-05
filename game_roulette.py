import random
import time
import db_manager  # الربط مع الخزنة والمهام والمخزون

MISSION_KEY = "roulette_win"  # مفتاح مهمة الروليت
REWARD_ITEM = "🎁 صندوق الحظ"

def handle(bot, message):
    if not message.text.startswith("روليت"):
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
            f"💸 رصيدك الحالي: {user_gold}\n"
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

    mission_completed_now = False

    # ───────── 4. النتائج ─────────
    if outcome == "win":
        db_manager.update_user_gold(uid, bet)
        new_bal = user_gold + bet

        mission_completed_now = db_manager.complete_mission(uid, MISSION_KEY)

        result_text = (
            "🟢 فوز!\n"
            f"💰 +{bet} ذهبة\n"
            f"✨ رصيدك الآن: {new_bal}"
        )

    elif outcome == "jackpot":
        jackpot = bet * 5
        db_manager.update_user_gold(uid, jackpot)
        new_bal = user_gold + jackpot

        mission_completed_now = db_manager.complete_mission(uid, MISSION_KEY)

        result_text = (
            "💥 جاكبوت أسطوري!\n"
            f"💰 +{jackpot} ذهبة\n"
            f"✨ رصيدك الآن: {new_bal}"
        )

    else:
        db_manager.update_user_gold(uid, -bet)
        new_bal = user_gold - bet

        result_text = (
            "🔴 خسارة!\n"
            f"💸 -{bet} ذهبة\n"
            f"💔 رصيدك الآن: {new_bal}"
        )

    bot.edit_message_text(
        result_text,
        chat_id=message.chat.id,
        message_id=status_msg.message_id
    )

    # ───────── 5. مكافأة إكمال المهمة ─────────
    if mission_completed_now:
        db_manager.add_item_to_inventory(uid, REWARD_ITEM, 1)

        bot.send_message(
            message.chat.id,
            "✅ تم إكمال المهمة بنجاح!\n\n"
            "🎁 تم إرسال صندوق الحظ إلى مخزونك\n"
            "📦 اكتب «مخزوني» لعرض المخزون"
        )
