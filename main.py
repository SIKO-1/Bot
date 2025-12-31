import os
import sqlite3
import random
import telebot
from telebot import types

# 1. الإعدادات
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEVELOPER_ID = 5860391324 

# 2. قاعدة البيانات
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, name TEXT, points INTEGER DEFAULT 0, level INTEGER DEFAULT 1, role TEXT DEFAULT 'عضو')")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked_games (user_id INTEGER, game_name TEXT)")
db.commit()

# 3. بنك الأسئلة الحقيقي (أضفت لك عينة حقيقية لكل نوع)
QUESTIONS = {
    "عواصم": [
        {"q": "ما هي عاصمة العراق؟", "a": "بغداد"},
        {"q": "ما هي عاصمة السعودية؟", "a": "الرياض"},
        {"q": "ما هي عاصمة فرنسا؟", "a": "باريس"}
    ],
    "رياضة": [
        {"q": "من هو الهداف التاريخي لكرة القدم؟", "a": "رونالدو"},
        {"q": "كم عدد لاعبي فريق كرة القدم؟", "a": "11"}
    ],
    "دين": [
        {"q": "كم عدد سور القرآن الكريم؟", "a": "114"},
        {"q": "ما هي أطول سورة في القرآن؟", "a": "البقرة"}
    ],
    "أنمي": [
        {"q": "من هو بطل أنمي ون بيس؟", "a": "لوفي"},
        {"q": "ما هو اسم بطل أنمي ناروتو؟", "a": "ناروتو"}
    ],
    "تحدي": [
        {"q": "شيء كلما زاد نقص؟", "a": "العمر"},
        {"q": "ما هو الشيء الذي له أسنان ولا يعض؟", "a": "المشط"}
    ]
}

# قائمة الألعاب وأسعارها (0 = مجانية)
GAMES_PRICE = {
    "عواصم": 0, "رياضة": 0, "دين": 0, "تحدي": 0,
    "أنمي": 1000, "أفلام": 1000, "برمجة": 2000
}

# 4. الأوامر
@bot.message_handler(func=lambda m: m.text in ["ايدي", "ا"])
def my_id(message):
    uid = message.from_user.id
    sql.execute("SELECT * FROM users WHERE user_id = ?", (uid,))
    u = sql.fetchone()
    if not u:
        sql.execute("INSERT INTO users (user_id, username, name) VALUES (?, ?, ?)", (uid, message.from_user.username, message.from_user.first_name))
        for g, p in GAMES_PRICE.items():
            if p == 0: sql.execute("INSERT INTO unlocked_games VALUES (?, ?)", (uid, g))
        db.commit(); return my_id(message)
    
    cap = f"<b>👤 معلوماتك:</b>\n\n<b>الاسم:</b> {u[2]}\n<b>النقاط:</b> {u[3]}\n<b>المستوى:</b> {u[4]}"
    bot.reply_to(message, cap)

@bot.message_handler(func=lambda m: m.text == "العاب")
def list_games(message):
    sql.execute("SELECT game_name FROM unlocked_games WHERE user_id = ?", (message.from_user.id,))
    unlocked = [r[0] for r in sql.fetchall()]
    txt = "🎮 <b>ألعاب الإمبراطورية:</b>\n\n"
    for g in GAMES_PRICE.keys():
        status = "✅" if g in unlocked else "🔒"
        txt += f"{status} {g}\n"
    bot.reply_to(message, txt + "\nأرسل اسم اللعبة لتبدأ.")

@bot.message_handler(func=lambda m: m.text == "المتجر")
def store(message):
    txt = "🛒 <b>متجر الألعاب:</b>\n\n"
    for g, p in GAMES_PRICE.items():
        if p > 0: txt += f"🔹 {g} ↫ {p} نقطة\n"
    bot.reply_to(message, txt + "\nللشراء أرسل: <b>شراء + اسم اللعبة</b>")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
def buy(message):
    game = message.text.split(" ", 1)[1]
    if game not in GAMES_PRICE: return bot.reply_to(message, "❌ هذه اللعبة غير موجودة.")
    
    sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
    user_pts = sql.fetchone()[0]
    price = GAMES_PRICE[game]
    
    if user_pts < price: return bot.reply_to(message, f"❌ نقاطك ({user_pts}) لا تكفي.")
    
    sql.execute("INSERT INTO unlocked_games VALUES (?, ?)", (message.from_user.id, game))
    sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (price, message.from_user.id))
    db.commit()
    bot.reply_to(message, f"🎉 مبروك! فتحت لعبة {game} بنجاح.")

@bot.message_handler(func=lambda m: m.text in QUESTIONS.keys())
def play(message):
    game = message.text
    sql.execute("SELECT * FROM unlocked_games WHERE user_id = ? AND game_name = ?", (message.from_user.id, game))
    if not sql.fetchone(): return bot.reply_to(message, "🔒 هذه اللعبة مقفولة، اشتريها من المتجر.")
    
    q = random.choice(QUESTIONS[game])
    m_sent = bot.reply_to(message, f"❓ {q['q']}")
    bot.register_next_step_handler(m_sent, check, q['a'])

def check(message, ans):
    if message.text == ans:
        sql.execute("UPDATE users SET points = points + 50 WHERE user_id = ?", (message.from_user.id,))
        db.commit()
        bot.reply_to(message, "✅ صح! حصلت على 50 نقطة.")
    else:
        bot.reply_to(message, f"❌ خطأ، الجواب هو: {ans}")

bot.infinity_polling()
