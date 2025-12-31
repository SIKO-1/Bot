import random
from telebot import types

# --- إعدادات الألعاب والأسعار والجوائز ---
GAMES_DATA = {
    "عواصم": {"buy": 200, "sell": 150, "win": 50, "rank": "عادية ⚪", "type": "buttons"},
    "رياضة": {"buy": 200, "sell": 150, "win": 50, "rank": "عادية ⚪", "type": "buttons"},
    "دين": {"buy": 200, "sell": 150, "win": 50, "rank": "عادية ⚪", "type": "text"},
    "ذكاء": {"buy": 200, "sell": 150, "win": 50, "rank": "عادية ⚪", "type": "buttons"},
    "تحدي": {"buy": 200, "sell": 150, "win": 50, "rank": "عادية ⚪", "type": "text"},
    "أفلام": {"buy": 400, "sell": 250, "win": 40, "rank": "ممتازة 🟢", "type": "buttons"},
    "جغرافيا": {"buy": 400, "sell": 250, "win": 40, "rank": "ممتازة 🟢", "type": "buttons"},
    "تاريخ": {"buy": 400, "sell": 250, "win": 40, "rank": "ممتازة 🟢", "type": "text"},
    "حيوانات": {"buy": 400, "sell": 250, "win": 40, "rank": "ممتازة 🟢", "type": "buttons"},
    "سيارات": {"buy": 400, "sell": 250, "win": 40, "rank": "ممتازة 🟢", "type": "buttons"},
    "أنمي": {"buy": 700, "sell": 550, "win": 30, "rank": "نادرة 🔵", "type": "buttons"},
    "ماركات": {"buy": 700, "sell": 550, "win": 30, "rank": "نادرة 🔵", "type": "buttons"},
    "طب": {"buy": 700, "sell": 550, "win": 30, "rank": "نادرة 🔵", "type": "text"},
    "فضاء": {"buy": 700, "sell": 550, "win": 30, "rank": "نادرة 🔵", "type": "buttons"},
    "علوم": {"buy": 700, "sell": 550, "win": 30, "rank": "نادرة 🔵", "type": "buttons"},
    "برمجة": {"buy": 900, "sell": 600, "win": 20, "rank": "أسطورية 🔥", "type": "buttons"},
    "فيزياء": {"buy": 900, "sell": 600, "win": 20, "rank": "أسطورية 🔥", "type": "text"},
    "كيمياء": {"buy": 900, "sell": 600, "win": 20, "rank": "أسطورية 🔥", "type": "buttons"},
    "أدب": {"buy": 900, "sell": 600, "win": 20, "rank": "أسطورية 🔥", "type": "buttons"},
    "فلسفة": {"buy": 900, "sell": 600, "win": 20, "rank": "أسطورية 🔥", "type": "buttons"},
    "هكر": {"buy": 2000, "sell": 1000, "win": 10, "rank": "فوق الأسطورية ✨", "type": "buttons"},
    "منطق": {"buy": 2000, "sell": 1000, "win": 10, "rank": "فوق الأسطورية ✨", "type": "text"},
    "حضارات": {"buy": 2000, "sell": 1000, "win": 10, "rank": "فوق الأسطورية ✨", "type": "buttons"},
    "الإمبراطور": {"buy": 5000, "sell": 0, "win": 5, "rank": "إمبراطورية 👑", "type": "buttons"},
    "الغاز_صعبة": {"buy": 5000, "sell": 0, "win": 5, "rank": "إمبراطورية 👑", "type": "text"}
}

# اختيار 5 ألعاب مجانية عشوائية
RANDOM_FREE_GAMES = random.sample(list(GAMES_DATA.keys()), 5)

# --- بنك الأسئلة (عينة شاملة لكل الألعاب) ---
QUESTIONS = {g: [{"q": f"سؤال {g} رقم {i}؟", "o": ["صح", "خطأ"], "a": "صح"} for i in range(1, 11)] for g in GAMES_DATA}

# تخصيص أمثلة حقيقية لضمان عمل الردود النصية والأزرار
QUESTIONS["عواصم"][0] = {"q": "عاصمة العراق؟", "o": ["بغداد", "دبي", "القاهرة"], "a": "بغداد"}
QUESTIONS["دين"][0] = {"q": "أطول سورة في القرآن؟", "a": "البقرة"}
QUESTIONS["تحدي"][0] = {"q": "ما هو حاصل 5+5؟", "a": "10"}

def get_games_menu(unlocked_list):
    txt = "✨ <b>إمبراطورية الألعاب</b> ✨\n\n"
    for name, info in GAMES_DATA.items():
        icon = "🔓" if (name in unlocked_list or name in RANDOM_FREE_GAMES) else "🔒"
        txt += f"{icon} <b>{name}</b> | {info['rank']}\n"
        txt += f"💰 ربح: {info['win']} | شراء: {info['buy']}\n\n"
    return txt

def start_game_logic(bot, message, game_name):
    q_data = random.choice(QUESTIONS[game_name])
    reward = GAMES_DATA[game_name]["win"]
    
    if GAMES_DATA[game_name]["type"] == "buttons":
        markup = types.InlineKeyboardMarkup()
        for opt in q_data["o"]:
            markup.add(types.InlineKeyboardButton(opt, callback_data=f"ans|{opt}|{q_data['a']}|{reward}"))
        bot.send_message(message.chat.id, f"🎮 <b>لعبة {game_name}:</b>\n\n❓ {q_data['q']}", reply_markup=markup)
    else:
        # نظام الرد النصي - يتم تسجيل الحالة في الـ main
        sent = bot.send_message(message.chat.id, f"📝 <b>لعبة {game_name}:</b>\n\n❓ {q_data['q']}\n\n(أرسل الإجابة بالرد على هذه الرسالة)")
        return q_data['a'], reward
