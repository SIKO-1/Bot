import os, sqlite3, random, telebot
from telebot import types

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324  # ايديك كمطور

# --- قاعدة البيانات ---
db = sqlite3.connect("kira_master.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT, points INTEGER DEFAULT 500)")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

# --- بنك البيانات والألعاب (25 لعبة) ---
GAMES_CONFIG = {
    # العاب مفتوحة (0 نقطة)
    "عواصم": {"price": 0, "rarity": "عادية ⚪"},
    "رياضة": {"price": 0, "rarity": "عادية ⚪"},
    "ذكاء": {"price": 0, "rarity": "عادية ⚪"},
    "دين": {"price": 0, "rarity": "عادية ⚪"},
    "تحدي": {"price": 0, "rarity": "عادية ⚪"},
    
    # العاب نادرة (2000 - 5000 نقطة)
    "أنمي": {"price": 2000, "rarity": "نادرة 🔵"},
    "أفلام": {"price": 2500, "rarity": "نادرة 🔵"},
    "تاريخ": {"price": 2000, "rarity": "نادرة 🔵"},
    "جغرافيا": {"price": 2000, "rarity": "نادرة 🔵"},
    "علوم": {"price": 3000, "rarity": "نادرة 🔵"},
    "سيارات": {"price": 3500, "rarity": "نادرة 🔵"},
    "ماركات": {"price": 3000, "rarity": "نادرة 🔵"},
    "فضاء": {"price": 4000, "rarity": "نادرة 🔵"},
    "حضارات": {"price": 4500, "rarity": "نادرة 🔵"},
    "أساطير": {"price": 5000, "rarity": "نادرة 🔵"},

    # العاب أسطورية (8000+ نقطة)
    "برمجة": {"price": 8000, "rarity": "أسطورية 🔥"},
    "هكر": {"price": 10000, "rarity": "أسطورية 🔥"},
    "طب": {"price": 9000, "rarity": "أسطورية 🔥"},
    "فيزياء": {"price": 8500, "rarity": "أسطورية 🔥"},
    "فلسفة": {"price": 9500, "rarity": "أسطورية 🔥"},
    "كيمياء": {"price": 8000, "rarity": "أسطورية 🔥"},
    "منطق": {"price": 9000, "rarity": "أسطورية 🔥"},
    "أدب": {"price": 7500, "rarity": "أسطورية 🔥"},
    "فن": {"price": 7000, "rarity": "أسطورية 🔥"},
    "الغاز_صعبة": {"price": 12000, "rarity": "إمبراطورية 👑"}
}

# توليد 15 سؤال لكل لعبة تلقائياً (يمكنك تخصيص الأجوبة لاحقاً)
QUESTIONS = {}
for game in GAMES_CONFIG.keys():
    QUESTIONS[game] = [
        {"q": f"سؤال في {game} رقم {i}؟", "o": ["إجابة 1", "إجابة 2", "إجابة 3"], "a": "إجابة 1"} 
        for i in range(1, 16)
    ]

# تخصيص عينة من الأسئلة الحقيقية
QUESTIONS["عواصم"][0] = {"q": "ما هي عاصمة اليابان؟", "o": ["طوكيو", "سيول", "بكين"], "a": "طوكيو"}
QUESTIONS["أنمي"][0] = {"q": "من هو صاحب 'مذكرة الموت'؟", "a": "لايت", "o": ["إل", "نيير", "لايت"]}

# --- الأوامر ---
@bot.message_handler(func=lambda m: m.text in ["ايدي", "ا"])
def my_id(message):
    uid = message.from_user.id
    sql.execute("INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)", (uid, message.from_user.first_name))
    sql.execute("SELECT points FROM users WHERE user_id = ?", (uid,))
    pts = sql.fetchone()[0]
    bot.reply_to(message, f"<b>👤 معلومات الإمبراطور:</b>\n\n<b>الاسم:</b> {message.from_user.first_name}\n<b>النقاط:</b> {pts}\n<b>الايدي:</b> <code>{uid}</code>")

@bot.message_handler(func=lambda m: m.text == "الاحصائيات" and m.from_user.id == DEV_ID)
def bot_stats(message):
    sql.execute("SELECT COUNT(*) FROM users")
    users_count = sql.fetchone()[0]
    bot.reply_to(message, f"📊 <b>إحصائيات الإمبراطورية:</b>\n\n👥 عدد الأعضاء: {users_count}\n🎮 عدد الألعاب: 25")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("رفع ") and m.from_user.id == DEV_ID)
def add_points_dev(message):
    try:
        pts = int(message.text.split()[1])
        uid = message.reply_to_message.from_user.id
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (pts, uid))
        db.commit()
        bot.reply_to(message, f"✅ تم إضافة {pts} نقطة للحساب.")
    except: bot.reply_to(message, "❌ رد على رسالة الشخص واكتب: رفع [العدد]")

@bot.message_handler(func=lambda m: m.text == "العاب")
def games_menu(message):
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (message.from_user.id,))
    unlocked_list = [r[0] for r in sql.fetchall()]
    txt = "🎮 <b>قائمة الألعاب (25 لعبة):</b>\n\n"
    for name, info in GAMES_CONFIG.items():
        status = "✅" if info['price'] == 0 or name in unlocked_list else "🔒"
        txt += f"{status} {name} ↫ {info['rarity']}\n"
    bot.reply_to(message, txt + "\nأرسل اسم اللعبة لتبدأ المتعة!")

@bot.message_handler(func=lambda m: m.text == "المتجر")
def store_menu(message):
    txt = "🛒 <b>متجر الإمبراطورية:</b>\n\n"
    for name, info in GAMES_CONFIG.items():
        if info['price'] > 0:
            txt += f"💎 {name} | {info['rarity']} ↫ {info['price']}ن\n"
    bot.reply_to(message, txt + "\nللشراء أرسل: <b>شراء اسم اللعبة</b>")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
def buy_game(message):
    game_name = message.text.replace("شراء ", "").strip()
    if game_name not in GAMES_CONFIG or GAMES_CONFIG[game_name]['price'] == 0: return
    
    sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
    user_pts = sql.fetchone()[0]
    price = GAMES_CONFIG[game_name]['price']
    
    if user_pts < price: return bot.reply_to(message, f"❌ نقاطك ({user_pts}) غير كافية لفتح {game_name}!")
    
    sql.execute("INSERT INTO unlocked VALUES (?, ?)", (message.from_user.id, game_name))
    sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (price, message.from_user.id))
    db.commit()
    bot.reply_to(message, f"🎉 مبروك! قمت بفتح لعبة <b>{game_name}</b> بنجاح.")

# --- نظام اللعب (Inline) ---
@bot.message_handler(func=lambda m: m.text in GAMES_CONFIG.keys())
def start_game(message):
    g = message.text
    if GAMES_CONFIG[g]['price'] > 0:
        sql.execute("SELECT * FROM unlocked WHERE user_id = ? AND game = ?", (message.from_user.id, g))
        if not sql.fetchone(): return bot.reply_to(message, "🔒 اللعبة مقفولة، اشتريها من المتجر أولاً.")
    
    q_data = random.choice(QUESTIONS[g])
    markup = types.InlineKeyboardMarkup()
    for opt in q_data['o']:
        markup.add(types.InlineKeyboardButton(opt, callback_data=f"game|{opt}|{q_data['a']}"))
    
    bot.send_message(message.chat.id, f"<b>🎮 لعبة: {g}</b>\n\n❓ {q_data['q']}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("game|"))
def handle_answer(call):
    _, user_ans, correct = call.data.split("|")
    if user_ans == correct:
        sql.execute("UPDATE users SET points = points + 50 WHERE user_id = ?", (call.from_user.id,))
        db.commit()
        bot.edit_message_text(f"✅ كفو! إجابتك صحيحة (+50 نقطة)\n\nالجواب: {correct}", call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text(f"❌ للأسف إجابة خاطئة!\n\nالجواب الصحيح: {correct}", call.message.chat.id, call.message.message_id)

bot.infinity_polling(skip_pending=True)
