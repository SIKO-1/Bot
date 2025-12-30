import os
import random
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")  # ضع توكن البوت
bot = telebot.TeleBot(TOKEN)

OWNER_ID = 5860391324  # مطور البوت كرار

# ================== قاعدة البيانات ==================
conn = sqlite3.connect("kira_bot.db", check_same_thread=False)
c = conn.cursor()

# جدول المستخدمين
c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    points INTEGER DEFAULT 0,
    money INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    messages INTEGER DEFAULT 0
)""")

# جدول الألعاب لكل مستخدم
c.execute("""CREATE TABLE IF NOT EXISTS user_games (
    user_id INTEGER,
    game_name TEXT
)""")

# جدول الأسئلة لكل لعبة
c.execute("""CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_name TEXT,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    answer INTEGER,
    points INTEGER
)""")

# جدول صح/خطأ
c.execute("""CREATE TABLE IF NOT EXISTS true_false_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_name TEXT,
    question TEXT,
    answer INTEGER,
    points INTEGER
)""")

# جدول الغزل لرحمة
c.execute("""CREATE TABLE IF NOT EXISTS rahma_poems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poem TEXT,
    type TEXT
)""")

conn.commit()

# ================== الألعاب ==================
ALL_GAMES = [
    "المختلف", "الأمثلة", "العكس", "الحزورة", "المعاني", "البات",
    "التخمين", "ترتيب", "السمايلات", "أسئلة", "صح/خطأ", "لو خيروك",
    "صراحة", "إعلام", "مقالات", "عواصم", "كلمات", "الحظ", "حظي",
    "عربي", "دين", "فكك", "حجره", "صور", "سيارات", "ايموجي",
    "اغاني", "تحدي", "المليون", "نشط عقلك", "XO"
]

# اقتباسات عشوائية للايدي
QUOTES = [
    "🌟 الحياة قصيرة، عشها بشغف!",
    "🌀 كن أنت التغيير الذي تريد أن تراه!",
    "🔥 القوي هو من يبتسم في وجه الألم!",
    "💫 الحلم الكبير يبدأ بخطوة صغيرة...",
    "🌈 لا تنتظر الفرصة، اصنعها بنفسك!",
    "⚡ النجاح يحتاج صبر وعزيمة!",
    "🌙 الليل ليس نهاية، بل بداية!",
    "💎 قيمة الإنسان في قلبه وعقله!",
    "🌹 من يعطي بدون انتظار يحصل على السلام!",
    "🌪️ العواصف تصنع الأبطال!",
    "🌊 من يغرق في الماضي لا يرى المستقبل!",
    "☀️ كل صباح فرصة جديدة!",
    "🗝️ المعرفة هي مفتاح الحرية!",
    "🕊️ التسامح يصنع السلام الداخلي!",
    "🎯 ركز على هدفك بلا خوف!",
    "🌟 التحدي يجعل الحياة مثيرة!",
    "💥 الفشل مجرد درس للنجاح!",
    "🌌 الكون واسع، فلتكن أحلامك أوسع!",
    "💡 فكرة صغيرة قد تغير حياتك!",
    "🛡️ الشجاعة الحقيقية في مواجهة الخوف!"
]

# ================== تعبئة قاعدة البيانات تلقائيًا ==================
def fill_db():
    # تعبئة الأسئلة لكل لعبة
    for game in ALL_GAMES:
        for i in range(1, 51):  # 50 سؤال لكل لعبة
            q = f"سؤال {i} للعبة {game}؟"
            o1 = f"خيار 1"
            o2 = f"خيار 2"
            o3 = f"خيار 3"
            ans = random.randint(1,3)
            pts = random.randint(3,10)
            c.execute("INSERT INTO questions (game_name, question, option1, option2, option3, answer, points) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (game, q, o1, o2, o3, ans, pts))
        for i in range(1, 41):  # 40 سؤال صح/خطأ لكل لعبة
            qtf = f"سؤال صح/خطأ {i} للعبة {game}؟"
            ans_tf = random.randint(0,1)
            pts_tf = random.randint(2,5)
            c.execute("INSERT INTO true_false_questions (game_name, question, answer, points) VALUES (?, ?, ?, ?)",
                      (game, qtf, ans_tf, pts_tf))
    # تعبئة الغزل
    poems_fusha = [f"بيت فصحى رقم {i} عن رحمة" for i in range(1,51)]
    poems_iraqi = [f"بيت عراقي رقم {i} عن رحمة" for i in range(1,51)]
    for p in poems_fusha:
        c.execute("INSERT INTO rahma_poems (poem, type) VALUES (?, ?)", (p, "fusha"))
    for p in poems_iraqi:
        c.execute("INSERT INTO rahma_poems (poem, type) VALUES (?, ?)", (p, "iraqi"))
    conn.commit()
    print("✅ تم تعبئة قاعدة البيانات بالكامل!")

fill_db()

# ================== وظائف أساسية ==================
def get_user(user):
    c.execute("SELECT * FROM users WHERE id=?", (user.id,))
    row = c.fetchone()
    if not row:
        c.execute(
            "INSERT INTO users (id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
            (user.id, user.username, user.first_name, user.last_name)
        )
        conn.commit()
        # 10 ألعاب مفتوحة تلقائيًا
        for g in ALL_GAMES[:10]:
            c.execute("INSERT INTO user_games (user_id, game_name) VALUES (?, ?)", (user.id, g))
        conn.commit()
        return get_user(user)
    return row

def increment_messages(user_id):
    c.execute("UPDATE users SET messages=messages+1 WHERE id=?", (user_id,))
    conn.commit()

def get_user_games(user_id):
    c.execute("SELECT game_name FROM user_games WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    return [r[0] for r in rows]

def add_points(user_id, pts):
    c.execute("UPDATE users SET points=points+?, money=money+? WHERE id=?", (pts, pts, user_id))
    c.execute("SELECT points FROM users WHERE id=?", (user_id,))
    points = c.fetchone()[0]
    level = min(999, points // 50 + 1)
    c.execute("UPDATE users SET level=? WHERE id=?", (level, user_id))
    conn.commit()

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    get_user(message.from_user)
    bot.send_message(message.chat.id, "👋 أهلًا بك في بوت كيرا الفخم!\nاكتب (اوامر) لعرض قائمة الأوامر")

# ================== قائمة الأوامر ==================
@bot.message_handler(func=lambda m: m.text.lower() in ["اوامر", "الأوامر"])
def commands(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🎮 الألعاب", callback_data="games"))
    keyboard.add(InlineKeyboardButton("💰 نقاطي", callback_data="mypoints"))
    keyboard.add(InlineKeyboardButton("🆔 معلوماتي", callback_data="myid"))
    if message.from_user.id == OWNER_ID:
        keyboard.add(InlineKeyboardButton("🛠 لوحة التحكم", callback_data="dashboard"))
    bot.send_message(message.chat.id, "📜 قائمة الأوامر:", reply_markup=keyboard)

# ================== ايدي فخم مزخرف ==================
@bot.message_handler(func=lambda m: m.text.lower() in ["ا", "ايدي"])
def my_id_command(message):
    user = get_user(message.from_user)
    increment_messages(user[0])
    games = get_user_games(user[0])
    games_text = ", ".join(games) if games else "لا يوجد"
    quote = random.choice(QUOTES)
    photos = bot.get_user_profile_photos(user[0], limit=1)
    text = f"""↫ دغيـرھَا لزڪـت بيـھَہّ 😡😕
⌁︙ايديـڪ↫ {user[0]}
⌁︙معرفـڪ↫ @{user[1] or 'لا يوجد'}
⌁︙حسابـڪ↫ عادي
⌁︙رتبتـڪ↫ العضـو
⌁︙تفاعلـڪ↫ سايق مخده 😹
⌁︙رسائلـڪ↫ {user[7]}
⌁︙نقاطـڪ↫ {user[4]}
⌁︙فلـوسـڪ↫ {user[5]}
⌁︙المستوى↫ {user[6]}
⌁︙الألعاب↫ {games_text}
⌁︙الاقتباس↫ {quote}"""
    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        bot.send_photo(message.chat.id, file_id, caption=text)
    else:
        bot.send_message(message.chat.id, text)

# ================== تفاعلات خاصة ==================
@bot.message_handler(func=lambda m: m.text.lower() == "كرار")
def uncle_krar(message):
    bot.reply_to(message, "عمك 😎")

@bot.message_handler(func=lambda m: m.text.lower() == "رحمه")
def rahma_poems_func(message):
    c.execute("SELECT poem FROM rahma_poems")
    poems = c.fetchall()
    if not poems:
        bot.reply_to(message, "💌 لا يوجد شعر مضاف بعد!")
        return
    keyboard = InlineKeyboardMarkup()
    # أضف أول 5 أبيات
    for i in range(min(5, len(poems))):
        keyboard.add(InlineKeyboardButton(poems[i][0], callback_data=f"poem_{i}"))
    keyboard.add(InlineKeyboardButton("المزيد 🔽", callback_data="more_poems"))
    bot.send_message(message.chat.id, "💌 غزل رحمة:", reply_markup=keyboard)

# ================== الألعاب ==================
@bot.callback_query_handler(func=lambda call: call.data=="games")
def show_games(call):
    user_games = get_user_games(call.from_user.id)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for game in ALL_GAMES:
        label = f"{game} {'🔒' if game not in user_games else ''}"
        keyboard.add(InlineKeyboardButton(label, callback_data=f"game_{game}"))
    bot.send_message(call.message.chat.id, "🎮 قائمة الألعاب:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("game_"))
def start_game(call):
    game_name = call.data[5:]
    user_games = get_user_games(call.from_user.id)
    if game_name not in user_games:
        bot.answer_callback_query(call.id, "❌ هذه اللعبة مقفولة! افتحها أولاً")
        return
    bot.send_message(call.message.chat.id, f"🎮 بدأت لعبة {game_name} (نظام نصي/اختيارات حسب اللعبة)")

# ================== تتبع الرسائل ==================
@bot.message_handler(func=lambda m: True)
def track_messages(message):
    get_user(message.from_user)
    increment_messages(message.from_user.id)

print("🔥 BOT KIRA IS RUNNING 🔥")
bot.infinity_polling()
