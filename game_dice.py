# game_dice.py
import random
import asyncio
from db_manager import get_inventory, update_user_points

COMMAND = "نرد"

async def handle(bot, message):
    if message.text != COMMAND:
        return

    uid = message.from_user.id
    inventory = await get_inventory(uid)

    # رسالة ترحيب مؤقتة
    await bot.send_message(message.chat.id, "🎲 جاري رمي نرد الإمبراطورية...\n⚔️ ركّز، فالحظ لا يبتسم مرتين.")

    # "رمي النرد"
    value = random.randint(1, 6)

    # تأثير درامي
    await asyncio.sleep(3.5)

    result_text = ""
    points_change = 0

    if value >= 5:
        # فوز إمبراطوري
        points_change = 20
        if "سيف الإمبراطور 🔱" in inventory:
            points_change = int(points_change * 1.2)
        if "قفاز القوة" in inventory:
            points_change = int(points_change * 1.25)
        if "خاتم الحظ 💍" in inventory and random.random() < 0.1:
            points_change += 5

        new_points = await update_user_points(uid, points_change)
        result_text = f"""
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ فـوز إمـبـراطـوري ⌯
┗━━━━━━━ ● ━━━━━━━┛

🔥 الحظ يبتسم لك : [ {value} ]
🏆 النقاط المكتسبة : +{points_change}
✨ رصيدك الحالي : {new_points} نقاط
        """

    elif value >= 3:
        # حظ متوسط
        points_change = 10
        if "سيف الإمبراطور 🔱" in inventory:
            points_change = int(points_change * 1.2)
        if "قفاز القوة" in inventory:
            points_change = int(points_change * 1.25)

        new_points = await update_user_points(uid, points_change)
        result_text = f"""
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ حظ متوسط ⌯
┗━━━━━━━ ● ━━━━━━━┛

🔥 الحظ يبتسم لك : [ {value} ]
🏆 النقاط المكتسبة : +{points_change}
✨ رصيدك الحالي : {new_points} نقاط
        """

    else:
        # خسارة
        points_change = -5
        if "درع الحصن 🛡️" in inventory:
            points_change = int(points_change * 0.5)
        if "عباءة الظلال 🧥" in inventory:
            points_change = int(points_change * 0.8)

        new_points = await update_user_points(uid, points_change)
        result_text = f"""
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ خسارة ساحقة ⌯
┗━━━━━━━ ● ━━━━━━━┛

💀 الحظ : [ {value} ]
💸 خسارتك : {abs(points_change)} نقاط
✨ رصيدك الحالي : {new_points} نقاط
        """

    # إرسال النتيجة النهائية
    await bot.send_message(message.chat.id, result_text)
