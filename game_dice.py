import time
import random
import db_manager

COMMAND = "نرد"
MISSION_TYPE = "play_dice"       # نوع المهمة للنرد
REWARD_ITEM = "🎁 صندوق الحظ النادر"

def handle(bot, message):
    if message.text != COMMAND:
        return

    uid = message.from_user.id
    inventory = db_manager.get_inventory(uid)

    # البداية
    start_msg = bot.reply_to(
        message,
        "🎲 جاري رمي نرد الإمبراطورية...\n"
        "⚔️ ركّز، فالحظ لا يبتسم مرتين."
    )

    # إرسال نرد Telegram
    dice_msg = bot.send_dice(message.chat.id)
    value = dice_msg.dice.value
    time.sleep(3.5)

    # النتائج
    if value >= 5:
        prize = 200
        if "سيف الإمبراطور" in inventory: prize = int(prize * 1.2)
        if "قفاز القوة" in inventory: prize = int(prize * 1.25)
        if "خاتم الحظ" in inventory and random.random() < 0.1: prize += 50

        new_gold = db_manager.update_user_gold(uid, prize)
        result_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ فـوز إمـبـراطـوري ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🔥 الحظ يبتسم لك : [ {value} ]\n"
            f"💰 الجائزة : +{prize} ذهب\n"
            f"✨ رصيدك الحالي : {new_gold} ذهب"
        )

    elif value >= 3:
        prize = 50
        if "سيف الإمبراطور" in inventory: prize = int(prize * 1.2)
        if "قفاز القوة" in inventory: prize = int(prize * 1.25)

        new_gold = db_manager.update_user_gold(uid, prize)
        result_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ حظ متوسط ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"🔥 الحظ يبتسم لك : [ {value} ]\n"
            f"💰 الجائزة : +{prize} ذهب\n"
            f"✨ رصيدك الحالي : {new_gold} ذهب"
        )

    else:
        penalty = -30
        if "درع الحصن" in inventory: penalty = int(penalty * 0.5)
        if "عباءة الظلال" in inventory: penalty = int(penalty * 0.8)

        new_gold = db_manager.update_user_gold(uid, penalty)
        result_text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ خسارة ساحقة ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"💀 الحظ : [ {value} ]\n"
            f"💸 خسارتك : {penalty} ذهب\n"
            f"✨ رصيدك الحالي : {new_gold} ذهب"
        )

    # إرسال النتيجة
    bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=dice_msg.message_id)

    # ======= تحقق من المهمة =======
    from daily_mission import check_task_completion
    check_task_completion(bot, message, MISSION_TYPE)
