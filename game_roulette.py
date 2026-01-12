# game_roulette.py
import random
import asyncio
from db_manager import get_user_points, update_user_points

COMMAND = "روليت"

async def handle(bot, message):
    if not message.text.startswith(COMMAND):
        return

    uid = message.from_user.id
    user_points = await get_user_points(uid)

    # ───────── 1. التحقق من الرهان ─────────
    parts = message.text.split(" ")
    if len(parts) < 2:
        await bot.send_message(message.chat.id, "⚠️ يجب تحديد مبلغ الرهان\n💡 مثال: روليت 50")
        return

    try:
        bet = int(parts[1])
    except:
        await bot.send_message(message.chat.id, "❌ الرهان يجب أن يكون رقماً صحيحاً")
        return

    if bet <= 0:
        await bot.send_message(message.chat.id, "🚫 لا يمكنك الرهان بمبلغ صفر أو أقل")
        return

    if bet > user_points:
        await bot.send_message(message.chat.id, f"💸 رصيدك الحالي: {user_points} نقاط\n❌ لا تملك نقاط كافية")
        return

    # ───────── 2. واجهة اللعب ─────────
    start_text = f"""
┏━━━━━━━ ● ━━━━━━━┓
      🎰 روليت الإمبراطورية 🎰
┗━━━━━━━ ● ━━━━━━━┛

💰 الرهان: {bet} نقاط
🌀 تدوير عجلة القدر...
    """
    status_msg = await bot.send_message(message.chat.id, start_text)

    await asyncio.sleep(1.5)
    await bot.edit_message_text(message.chat.id, status_msg.message_id, start_text + "\n\n⚡️ العجلة تتباطأ...")
    await asyncio.sleep(1.5)

    # ───────── 3. تحديد النتيجة ─────────
    outcome = ["win", "lose", "jackpot"]
    weights = [45, 50, 5]

    def weighted_random(items, weights):
        total = sum(weights)
        r = random.uniform(0, total)
        for i, w in enumerate(weights):
            if r < w:
                return items[i]
            r -= w
        return items[-1]

    result = weighted_random(outcome, weights)

    # ───────── 4. النتائج ─────────
    new_points = user_points
    result_text = ""

    if result == "win":
        new_points = await update_user_points(uid, bet)
        result_text = f"""
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ فـوز إمـبـراطـوري ⌯
┗━━━━━━━ ● ━━━━━━━┛

🔥 الحظ يبتسم لك : [ الفوز ]
🏆 النقاط المكتسبة : +{bet}
✨ رصيدك الحالي : {new_points} نقاط
        """
    elif result == "jackpot":
        jackpot = bet * 5
        new_points = await update_user_points(uid, jackpot)
        result_text = f"""
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ جاكبوت أسطوري ⌯
┗━━━━━━━ ● ━━━━━━━┛

🔥 الحظ يبتسم لك : [ الجاكبوت ]
🏆 النقاط المكتسبة : +{jackpot}
✨ رصيدك الحالي : {new_points} نقاط
        """
    else:  # lose
        new_points = await update_user_points(uid, -bet)
        result_text = f"""
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ خسارة ساحقة ⌯
┗━━━━━━━ ● ━━━━━━━┛

💀 الحظ : [ الخسارة ]
💸 خسارتك : -{bet} نقاط
✨ رصيدك الحالي : {new_points} نقاط
        """

    await bot.edit_message_text(message.chat.id, status_msg.message_id, result_text)
