import time
import random
import db_manager

COMMAND = "نرد"

MISSION_KEY = "dice_win"      # مفتاح مهمة النرد
REWARD_ITEM = "🎁 صندوق الحظ"

def handle(bot, message):
    if message.text != COMMAND:
        return

    uid = message.from_user.id
    inventory = db_manager.get_inventory(uid)

    start_msg = bot.reply_to(
        message,
        "🎲 جاري رمي نرد الإمبراطورية...\n"
        "⚔️ ركّز، فالحظ لا يبتسم مرتين."
    )

    dice_msg = bot.send_dice(message.chat.id)
    value = dice_msg.dice.value

    time.sleep(3.5)

    mission_completed_now = False

    # ───────── نتائج النرد ─────────
    if value >= 5:
        prize = 200

        if "سيف الإمبراطور" in inventory:
            prize = int(prize * 1.2)

        if "قفاز القوة" in inventory:
            prize = int(prize * 1.25)

        if "خاتم الحظ" in inventory and random.random() < 0.1:
            prize += 50

        new_gold = db_manager.update_user_gold(uid, prize)

        # محاولة إكمال المهمة
        mission_completed_now = db_manager.complete_mission(uid, MISSION_KEY)

        res_text = (
            "🏆 فوز إمبراطوري!\n"
            f"🎲 النرد: {value}\n"
            f"💰 +{prize} ذهب\n"
            f"✨ رصيدك الآن: {new_gold} ذهب"
        )

    elif value >= 3:
        prize = 50

        if "سيف الإمبراطور" in inventory:
            prize = int(prize * 1.2)

        if "قفاز القوة" in inventory:
            prize = int(prize * 1.25)

        new_gold = db_manager.update_user_gold(uid, prize)

        res_text = (
            "⚖️ حظ متوسط\n"
            f"🎲 النرد: {value}\n"
            f"💰 +{prize} ذهب\n"
            f"✨ رصيدك الآن: {new_gold} ذهب"
        )

    else:
        penalty = -30

        if "درع الحصن" in inventory:
            penalty = int(penalty * 0.5)

        if "عباءة الظلال" in inventory:
            penalty = int(penalty * 0.8)

        new_gold = db_manager.update_user_gold(uid, penalty)

        res_text = (
            "💀 خسارة موجعة\n"
            f"🎲 النرد: {value}\n"
            f"💸 {penalty} ذهب\n"
            f"💔 رصيدك الآن: {new_gold} ذهب"
        )

    # عرض نتيجة اللعب
    bot.reply_to(dice_msg, res_text)

    # حذف رسالة البداية
    try:
        bot.delete_message(message.chat.id, start_msg.message_id)
    except:
        pass

    # ───────── مكافأة إكمال المهمة ─────────
    if mission_completed_now:
        db_manager.add_item_to_inventory(uid, REWARD_ITEM, 1)

        bot.send_message(
            message.chat.id,
            "✅ تم إكمال المهمة!\n\n"
            "🎁 تم إرسال صندوق الحظ إلى مخزونك\n"
            "📦 اكتب «مخزوني» لعرض المخزون"
        )
