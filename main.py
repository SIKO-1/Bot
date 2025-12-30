import os
import random
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

OWNER_ID = 5860391324  # كرار المطور

# ================== قاعدة البيانات ==================
conn = sqlite3.connect("kira_bot.db", check_same_thread=False)
c = conn.cursor()

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

c.execute("""CREATE TABLE IF NOT EXISTS user_games (
    user_id INTEGER,
    game_name TEXT
)""")

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

c.execute("""CREATE TABLE IF NOT EXISTS true_false_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_name TEXT,
    question TEXT,
    answer INTEGER,
    points INTEGER
)""")

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
    "اغاني", "تحدي", "المليون", "نشط عقلك", "XO", "رياضيات", "انكليزي",
    "كت تويت", "لو خيروك2", "صراحة2", "اغاني2", "معاني2", "حروف", "لوحة", 
    "تحدي2", "ذكاء", "حظ2", "اكواد", "لغز2", "ترتيب2", "صور2", "حجره2", "فكك2"
]

GAME_POINTS = {game: random.randint(3,10) for game in ALL_GAMES}  # نقاط مختلفة لكل لعبة

QUOTES = [
    "🌟 الحياة قصيرة، عشها بشغف!",
    "🌀 كن أنت التغيير الذي تريد أن تراه!",
    "🔥 القوي هو من يبتسم في وجه الألم!",
    "💫 الحلم الكبير يبدأ بخطوة صغيرة...",
    "🌈 لا تنتظر الفرصة، اصنعها بنفسك!"
]

# ================== تعبئة قاعدة البيانات ==================
def fill_db_once():
    c.execute("SELECT COUNT(*) FROM questions")
    if c.fetchone()[0] == 0:
        for game in ALL_GAMES:
            for i in range(1, 51):
                q = f"سؤال {i} للعبة {game}؟"
                o1, o2, o3 = "خيار 1", "خيار 2", "خيار 3"
                ans = random.randint(1,3)
                pts = GAME_POINTS[game]
                c.execute("INSERT INTO questions (game_name, question, option1, option2, option3, answer, points) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (game, q, o1, o2, o3, ans, pts))
            for i in range(1, 41):
                qtf = f"سؤال صح/خطأ {i} للعبة {game}؟"
                ans_tf = random.randint(0,1)
                pts_tf = GAME_POINTS[game]
                c.execute("INSERT INTO true_false_questions (game_name, question, answer, points) VALUES (?, ?, ?, ?)",
                          (game, qtf, ans_tf, pts_tf))
        poems_fusha = [f"بيت فصحى رقم {i} عن رحمة" for i in range(1,51)]
        poems_iraqi = [f"بيت عراقي رقم {i} عن رحمة" for i in range(1,51)]
        for p in poems_fusha: c.execute("INSERT INTO rahma_poems (poem, type) VALUES (?, ?)", (p, "fusha"))
        for p in poems_iraqi: c.execute("INSERT INTO rahma_poems (poem, type) VALUES (?, ?)", (p, "iraqi"))
        conn.commit()
        print("✅ تم تعبئة قاعدة البيانات لأول مرة!")

fill_db_once()

# ================== وظائف المستخدم ==================
def get_user(user):
    c.execute("SELECT * FROM users WHERE id=?", (user.id,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO users (id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
                  (user.id, user.username, user.first_name, user.last_name))
        conn.commit()
        for g in ALL_GAMES[:10]:
            c.execute("INSERT INTO user_games (user_id, game_name) VALUES (?, ?)", (user.id, g))
        conn.commit()
        c.execute("SELECT * FROM users WHERE id=?", (user.id,))
        row = c.fetchone()
    return row

def increment_messages(user_id):
    c.execute("UPDATE users SET messages=messages+1 WHERE id=?", (user_id,))
    conn.commit()

def get_user_games(user_id):
    c.execute("SELECT game_name FROM user_games WHERE user_id=?", (user_id,))
    return [r[0] for r in c.fetchall()]

def add_points(user_id, points):
    c.execute("UPDATE users SET points=points+? WHERE id=?", (points, user_id))
    conn.commit()

def level_up(user_id, levels=1):
    c.execute("UPDATE users SET level=level+? WHERE id=?", (levels, user_id))
    conn.commit()

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    get_user(message.from_user)
    bot.send_message(message.chat.id, "👋 أهلًا بك في بوت كيرا الفخم!\nاكتب (اوامر) لعرض قائمة الأوامر")

# ================== قائمة الأوامر ==================
@bot.message_handler(func=lambda m: m.text.lower() in ["اوامر", "الأوامر"])
def commands(message):
    text = """📜 قائمة الأوامر الفخمة:
- 🎮 الألعاب: اكتب اسم اللعبة لتشغيلها
- 💰 نقاطي: لعرض نقاطك وفلوسك
- 🆔 ا / ايدي: لعرض معلوماتك
- 🛠 لوحة التحكم (للمطور فقط)
"""
    bot.send_message(message.chat.id, text)

# ================== ايدي مزخرف ==================
@bot.message_handler(func=lambda m: m.text.lower() in ["ا", "ايدي"])
def my_id_command(message):
    user = get_user(message.from_user)
    increment_messages(user[0])
    games = get_user_games(user[0])
    games_text = ", ".join(games) if games else "لا يوجد"
    quote = random.choice(QUOTES)
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
⌁︙اقتباس↫ {quote}"""
    bot.send_message(message.chat.id, text)

# ================== أوامر خاصة ==================
@bot.message_handler(func=lambda m: m.text.lower() == "كرار")
def uncle_krar(message):
    bot.reply_to(message, "عمك 😎")

@bot.message_handler(func=lambda m: m.text.lower() == "رحمه")
def rahma_poems_func(message):
    if message.from_user.id != OWNER_ID:
        return
    c.execute("SELECT poem FROM rahma_poems")
    poems = c.fetchall()
    text = "💌 غزل رحمة:\n" + "\n".join([p[0] for p in poems[:5]]) + "\n... المزيد بالضغط على أمر 'رحمه' مرة أخرى"
    bot.send_message(message.chat.id, text)

# ================== تشغيل الألعاب ==================
@bot.message_handler(func=lambda m: m.text in ALL_GAMES)
def play_game(message):
    user_games = get_user_games(message.from_user.id)
    game_name = message.text
    if game_name not in user_games:
        bot.send_message(message.chat.id, "❌ هذه اللعبة مقفولة! افتحها أولاً")
        return
    # الألعاب التي تحتاج InlineKeyboard
    if game_name in ["أسئلة", "صح/خطأ", "XO"]:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("مثال خيار 1", callback_data="choice1"))
        markup.add(InlineKeyboardButton("مثال خيار 2", callback_data="choice2"))
        bot.send_message(message.chat.id, f"🎮 بدأت لعبة {game_name}:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"🎮 بدأت لعبة {game_name} (نصية)")

# ================== تتبع الرسائل ==================
@bot.message_handler(func=lambda m: True)
def track_messages(message):
    get_user(message.from_user)
    increment_messages(message.from_user.id)

print("🔥 BOT KIRA FULL VERSION RUNNING 🔥")
bot.infinity_polling()
