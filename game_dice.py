import time
from db_manager import get_user_gold, update_user_gold

COMMAND = "نرد"

def handle(bot, message):
    if message.text != COMMAND:
        return

    uid = message.from_user.id
    user_gold = get_user_gold(uid)

    start_msg = bot.reply_to(message, "🎲 جاري رمي نرد الحظ الإمبراطوري... استعد!")

    dice_msg = bot.send_dice(message.chat.id)
    value = dice_msg.dice.value

    time.sleep(3.5)

    if value >= 5:
        prize = 200
        update_user_gold(uid, prize)
        res_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ فـوز إمـبـراطـوري ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🔥 الحظ يبتسم لك : [ {value} ]\n"
            f"💰 الجائزة : +{prize} ذهب\n"
            f"✨ رصيدك الحالي : {user_gold + prize}"
        )
    elif value >= 3:
        prize = 50
        update_user_gold(uid, prize)
        res_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ حظ متوسط ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🎲 النتيجة مقبولة : [ {value} ]\n"
            f"💰 الجائزة : +{prize} ذهب\n"
            f"✨ رصيدك الحالي : {user_gold + prize}"
        )
    else:
        penalty = -30
        update_user_gold(uid, penalty)
        res_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ غضب النرد ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🌚 للأسف حظك عاثر : [ {value} ]\n"
            f"💸 ضريبة الحظ : {penalty} ذهب\n"
            f"✨ رصيدك الحالي : {max(0, user_gold + penalty)}"
        )

    bot.reply_to(dice_msg, res_text)

    try:
        bot.delete_message(message.chat.id, start_msg.message_id)
    except:
        pass
