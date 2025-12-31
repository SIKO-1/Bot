import random
from telebot import types

# تأكد من وجود ألعاب كافية (أو سيختار الكود المتاح فقط)
GAMES_DATA = {
    "عواصم": {"buy": 200, "win": 50, "type": "buttons"},
    "رياضة": {"buy": 200, "win": 50, "type": "buttons"},
    "دين": {"buy": 200, "win": 50, "type": "text"},
    "ذكاء": {"buy": 200, "win": 50, "type": "buttons"},
    "تحدي": {"buy": 200, "win": 50, "type": "text"},
}

# إصلاح خطأ الانهيار: اختيار 5 ألعاب أو أقل إذا لم تتوفر
count = min(len(GAMES_DATA), 5)
RANDOM_FREE_GAMES = random.sample(list(GAMES_DATA.keys()), count)

QUESTIONS = {g: [{"q": f"سؤال في {g}؟", "o": ["أ", "ب"], "a": "أ"}] for g in GAMES_DATA}

def get_games_menu(unlocked_list):
    txt = "🎭 <b>إمبراطورية الألعاب</b>\n"
    for name, info in GAMES_DATA.items():
        status = "🔓" if (name in unlocked_list or name in RANDOM_FREE_GAMES) else "🔒"
        txt += f"{status} {name} | ربح: {info['win']}ن\n"
    return txt

def start_game_logic(bot, message, game_name):
    q = random.choice(QUESTIONS[game_name])
    markup = types.InlineKeyboardMarkup()
    for o in q.get("o", ["صح"]):
        markup.add(types.InlineKeyboardButton(o, callback_data=f"ans|{o}|{q['a']}"))
    bot.send_message(message.chat.id, f"🎮 {game_name}:\n\n❓ {q['q']}", reply_markup=markup)
