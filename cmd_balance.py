# cmd_balance.py
from db_manager import get_user_gold, get_user_points

COMMANDS = ["فلوسي", "نقاطي"]

def handle(bot, update):
    text = update.message.text.strip()
    if not text or text not in COMMANDS:
        return

    uid = update.message.from_user.id
    gold = get_user_gold(uid) or 0
    points = get_user_points(uid) or 0

    if gold == 0 and points == 0:
        bot.send_message(
            chat_id=update.message.chat.id,
            text="⌔︙ليس لديك نقاط أو فلوس، أرسل الألعاب وابدأ اللعب!"
        )
    else:
        bot.send_message(
            chat_id=update.message.chat.id,
            text=f"⌔︙عدد نقاطك: {points}\n فلوسك: {gold}"
        )
