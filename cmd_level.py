from db_manager import get_user_gold

COMMANDS = ["مستوى", "لفلي", "lv"]

def handle(bot, message):
    if message.text not in COMMANDS:
        return

    uid = message.from_user.id
    gold = get_user_gold(uid)

    # كل 50 ذهب = مستوى واحد
    level = gold // 50

    # حساب التقدم للمستوى القادم
    next_level_gold = ((level + 1) * 50)
    remaining = max(0, next_level_gold - gold)

    # ألقاب بسيطة حسب المستوى
    if level < 10:
        title = "مبتدئ الإمبراطورية"
    elif level < 50:
        title = "محارب الظل"
    elif level < 100:
        title = "سيد الساحة"
    else:
        title = "أسطورة كيرا"

    text = (
        "╔═════════════════╗\n"
        "      المستوى\n"
        "╚═════════════════╝\n\n"
        f"↫ مستواك ↫ {level}\n"
        f"↫ لقبك ↫ {title}\n"
        f"↫ رصيدك ↫ {gold} ذهب\n"
        f"↫ للمستوى القادم ↫ {remaining} ذهب"
    )

    bot.reply_to(message, text)
