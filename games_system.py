import random
from telebot import types

# بيانات الـ 25 لعبة
GAMES_DATA = {
    "عواصم": {"buy": 200, "win": 50, "type": "buttons"},
    "رياضة": {"buy": 200, "win": 50, "type": "buttons"},
    "دين": {"buy": 200, "win": 50, "type": "text"},
    # ... (تكملة الـ 25 لعبة بنفس النمط)
}

RANDOM_FREE_GAMES = random.sample(list(GAMES_DATA.keys()), 5)

QUESTIONS = {g: [{"q": f"سؤال في {g}؟", "o": ["أ", "ب"], "a": "أ"}] for g in GAMES_DATA}

def get_games_menu(unlocked_list):
    txt = "🎭 <b>إمبراطورية الألعاب</b>\n"
    for name, info in GAMES_DATA.items():
        status = "🔓" if (name in unlocked_list or name in RANDOM_FREE_GAMES) else "🔒"
        txt += f"{status} {name} | ربح: {info['win']}ن\n"
    return txt

def start_game_logic(bot, message, game_name):
    q = random.choice(QUESTIONS[game_name])
    reward = GAMES_DATA[game_name]["win"]
    markup = types.InlineKeyboardMarkup()
    for o in q["o"]:
        markup.add(types.InlineKeyboardButton(o, callback_data=f"ans|{o}|{q['a']}|{reward}"))
    bot.send_message(message.chat.id, f"🎮 {game_name}:\n\n❓ {q['q']}", reply_markup=markup)
