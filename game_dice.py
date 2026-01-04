import time
from db_manager import get_user_gold, update_user_gold, get_inventory
import random

COMMAND = "نرد"

def handle(bot, message):
    if message.text != COMMAND:
        return

    uid = message.from_user.id
    inventory = get_inventory(uid)

    start_msg = bot.reply_to(message, "🎲 جاري رمي نرد الحظ الإمبراطوري... استعد!")

    dice_msg = bot.send_dice(message.chat.id)
    value = dice_msg.dice.value

    time.sleep(3.5)

    # تحسب الرصيد بعد التأثيرات
    if value >= 5:
        prize = 200
        # تأثيرات الأغراض
        if "سيف الإمبراطور" in inventory:
            prize = int(prize * 1.2)
        if "قفاز القوة" in inventory:
            prize = int(prize * 1.25)
        if "خاتم الحظ" in inventory and random.random() < 0.1:  # فرصة 10%
            prize += 50
        new_gold = update_user_gold(uid, prize)
        res_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ فـوز إمـبـراطـوري ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🔥 الحظ يبتسم لك : [ {value} ]\n"
            f"💰 الجائزة : +{prize} ذهب\n"
            f"✨ رصيدك الحالي : {new_gold}"
        )

    elif value >= 3:
        prize = 50
        if "سيف الإمبراطور" in inventory:
            prize = int(prize * 1.2)
        if "قفاز القوة" in inventory:
            prize = int(prize * 1.25)
        new_gold = update_user_gold(uid, prize)
        res_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ حظ متوسط ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🎲 النتيجة مقبولة : [ {value} ]\n"
            f"💰 الجائزة : +{prize} ذهب\n"
            f"✨ رصيدك الحالي : {new_gold}"
        )

    else:
        penalty = -30
        if "درع الحصن" in inventory:
            penalty = int(penalty * 0.5)
        if "عباءة الظلال" in inventory:
            penalty = int(penalty * 0.8)
        new_gold = update_user_gold(uid, penalty)
        res_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ غضب النرد ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🌚 للأسف حظك عاثر : [ {value} ]\n"
            f"💸 ضريبة الحظ : {penalty} ذهب\n"
            f"✨ رصيدك الحالي : {max(0, new_gold)}"
        )

    bot.reply_to(dice_msg, res_text)

    try:
        bot.delete_message(message.chat.id, start_msg.message_id)
    except:
        pass
