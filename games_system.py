import random
from telebot import types

# الإعدادات لـ 25 لعبة مع الأسعار والنسب التنازلية
GAMES_DATA = {
    "عواصم": {"buy": 200, "win": 50, "rank": "عادية", "type": "buttons"},
    "رياضة": {"buy": 200, "win": 50, "rank": "عادية", "type": "buttons"},
    "دين": {"buy": 200, "win": 50, "rank": "عادية", "type": "text"},
    "ذكاء": {"buy": 200, "win": 50, "rank": "عادية", "type": "buttons"},
    "تحدي": {"buy": 200, "win": 50, "rank": "عادية", "type": "text"},
    "أفلام": {"buy": 400, "win": 40, "rank": "ممتازة", "type": "buttons"},
    "جغرافيا": {"buy": 400, "win": 40, "rank": "ممتازة", "type": "buttons"},
    "تاريخ": {"buy": 400, "win": 40, "rank": "ممتازة", "type": "text"},
    "حيوانات": {"buy": 400, "win": 40, "rank": "ممتازة", "type": "buttons"},
    "سيارات": {"buy": 400, "win": 40, "rank": "ممتازة", "type": "buttons"},
    "أنمي": {"buy": 700, "win": 30, "rank": "نادرة", "type": "buttons"},
    "ماركات": {"buy": 700, "win": 30, "rank": "نادرة", "type": "buttons"},
    "طب": {"buy": 700, "win": 30, "rank": "نادرة", "type": "text"},
    "فضاء": {"buy": 700, "win": 30, "rank": "نادرة", "type": "buttons"},
    "علوم": {"buy": 700, "win": 30, "rank": "نادرة", "type": "buttons"},
    "برمجة": {"buy": 900, "win": 20, "rank": "أسطورية", "type": "buttons"},
    "فيزياء": {"buy": 900, "win": 20, "rank": "أسطورية", "type": "text"},
    "كيمياء": {"buy": 900, "win": 20, "rank": "أسطورية", "type": "buttons"},
    "أدب": {"buy": 900, "win": 20, "rank": "أسطورية", "type": "buttons"},
    "فلسفة": {"buy": 900, "win": 20, "rank": "أسطورية", "type": "buttons"},
    "هكر": {"buy": 2000, "win": 10, "rank": "فوق أسطورية", "type": "buttons"},
    "منطق": {"buy": 2000, "win": 10, "rank": "فوق أسطورية", "type": "text"},
    "حضارات": {"buy": 2000, "win": 10, "rank": "فوق أسطورية", "type": "buttons"},
    "الإمبراطور": {"buy": 5000, "win": 5, "rank": "إمبراطورية", "type": "buttons"},
    "الغاز_صعبة": {"buy": 5000, "win": 5, "rank": "إمبراطورية", "type": "text"}
}

RANDOM_FREE_GAMES = random.sample(list(GAMES_DATA.keys()), 5)

QUESTIONS = {g: [{"q": f"سؤال في {g} رقم {i}؟", "o": ["صح", "خطأ"], "a": "صح"} for i in range(1, 11)] for g in GAMES_DATA}

def get_games_menu(unlocked_list):
    txt = "🎭 <b>قائمة الألعاب:</b>\n"
    for name, info in GAMES_DATA.items():
        icon = "🔓" if (name in unlocked_list or name in RANDOM_FREE_GAMES) else "🔒"
        txt += f"{icon} {name} | {info['rank']} | ربح: {info['win']}ن\n"
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
