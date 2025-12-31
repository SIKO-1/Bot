import random
from telebot import types

GAMES_DATA = {
    "عواصم": {"buy": 200, "win": 50, "type": "buttons"},
    "دين": {"buy": 200, "win": 50, "type": "text"},
    "أنمي": {"buy": 700, "win": 30, "type": "buttons"},
    # ... (باقي الـ 25 لعبة بنفس النمط مع النسب التنازلية)
}

# اختيار 5 ألعاب مجانية عشوائية عند كل تشغيل
RANDOM_FREE_GAMES = random.sample(list(GAMES_DATA.keys()), 5 if len(GAMES_DATA) >= 5 else len(GAMES_DATA))

# بنك الأسئلة (10 أسئلة لكل لعبة)
QUESTIONS = {g: [{"q": f"سؤال في {g} - المرحلة {i}؟", "o": ["صح", "خطأ"], "a": "صح"} for i in range(1, 11)] for g in GAMES_DATA}

def get_games_menu(unlocked_list):
    txt = "🎭 <b>قائمة الألعاب:</b>\n"
    for name, info in GAMES_DATA.items():
        icon = "🔓" if (name in unlocked_list or name in RANDOM_FREE_GAMES) else "🔒"
        txt += f"{icon} {name} | ربح: {info['win']}ن\n"
    return txt

def start_game_logic(bot, message, game_name):
    q = random.choice(QUESTIONS[game_name])
    if GAMES_DATA[game_name]["type"] == "buttons":
        markup = types.InlineKeyboardMarkup()
        for o in q["o"]:
            markup.add(types.InlineKeyboardButton(o, callback_data=f"ans|{o}|{q['a']}"))
        bot.send_message(message.chat.id, f"🎮 {game_name}:\n\n❓ {q['q']}", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"📝 {game_name}:\n\n❓ {q['q']}\n(أجب بالرد)")
