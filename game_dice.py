import time
import random
from db_manager import get_user_gold, update_user_gold, get_inventory

COMMAND = "نرد"

def handle(bot, message):
    if message.text != COMMAND:
        return

    uid = message.from_user.id
    inventory = get_inventory(uid)

    start_msg = bot.reply_to(message, "🎲 جاري رمي نرد الإمبراطوري... استعد!")

    dice_msg = bot.send_dice(message.chat.id)
    value = dice_msg.dice.value
    time.sleep(3.5)

    # رصيد بعد تطبيق التأثيرات
    if value >= 5:
        prize = 200
        if "سيف الإمبراطور" in inventory: prize = int(prize * 1.2)
        if "قفاز القوة" in inventory: prize = int(prize * 1.25)
        if "خاتم الحظ" in inventory and random.random() < 0.1: prize += 50
        new_gold = update_user_gold(uid, prize)
        res_text = f"🏆 فوز إمبراطوري! +{prize} ذهب\nرصيدك الآن: {new_gold} ذهب"

    elif value >= 3:
        prize = 50
        if "سيف الإمبراطور" in inventory: prize = int(prize * 1.2)
        if "قفاز القوة" in inventory: prize = int(prize * 1.25)
        new_gold = update_user_gold(uid, prize)
        res_text = f"✅ حظ متوسط! +{prize} ذهب\nرصيدك الآن: {new_gold} ذهب"

    else:
        penalty = -30
        if "درع الحصن" in inventory: penalty = int(penalty * 0.5)
        if "عباءة الظلال" in inventory: penalty = int(penalty * 0.8)
        new_gold = update_user_gold(uid, penalty)
        res_text = f"💀 خسارة! {penalty} ذهب\nرصيدك الآن: {new_gold} ذهب"

    bot.reply_to(dice_msg, res_text)
    try: bot.delete_message(message.chat.id, start_msg.message_id)
    except: pass
