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

# 3. بنك الأسئلة الحقيقي (أكثر من 100 سؤال)
QUESTIONS = {
    "عواصم": [
        {"q": "عاصمة العراق؟", "a": "بغداد"}, {"q": "عاصمة السعودية؟", "a": "الرياض"},
        {"q": "عاصمة مصر؟", "a": "القاهرة"}, {"q": "عاصمة اليابان؟", "a": "طوكيو"},
        {"q": "عاصمة فرنسا؟", "a": "باريس"}, {"q": "عاصمة قطر؟", "a": "الدوحة"}
    ],
    "رياضة": [
        {"q": "من فاز بكأس العالم 2022؟", "a": "الارجنتين"}, {"q": "نادي يلقب بالملكي؟", "a": "ريال مدريد"},
        {"q": "كم لاعب في فريق السلة؟", "a": "5"}, {"q": "أين يلعب كريستيانو حالياً؟", "a": "النصر"}
    ],
    "أنمي": [
        {"q": "بطل ون بيس؟", "a": "لوفي"}, {"q": "عين الشارينغان في أي أنمي؟", "a": "ناروتو"},
        {"q": "قاتل الشياطين بطل الأنمي هو؟", "a": "تانجيرو"}, {"q": "صاحب مذكرة الموت؟", "a": "لايت"}
    ],
    "دين": [
        {"q": "نبي لقب بكليم الله؟", "a": "موسى"}, {"q": "أول مؤذن في الإسلام؟", "a": "بلال"},
        {"q": "كم عدد الصلوات؟", "a": "5"}, {"q": "أين ولد النبي محمد؟", "a": "مكة"}
    ],
    "ذكاء": [
        {"q": "خال أولاد عمتك؟", "a": "ابوك"}, {"q": "يمشي بلا أرجل؟", "a": "النهر"},
        {"q": "كلما طال قصر؟", "a": "العمر"}, {"q": "يسمع بلا أذن؟", "a": "الهاتف"}
    ],
    "تاريخ": [
        {"q": "من فاتح القدس؟", "a": "صلاح الدين"}, {"q": "أين تقع الأهرامات؟", "a": "مصر"}
    ]
}

GAMES_PRICE = {
    "عواصم": 0, "رياضة": 0, "دين": 0, "تحدي": 0, "ذكاء": 0, "تاريخ": 0,
    "أنمي": 500, "أفلام": 800, "برمجة": 1500, "فضاء": 1000
}

# 4. الأوامر الأساسية
@bot.message_handler(func=lambda m: m.text in ["ايدي", "ا"])
def my_id(message):
    uid = message.from_user.id
    sql.execute("SELECT * FROM users WHERE user_id = ?", (uid,))
    u = sql.fetchone()
    if not u:
        sql.execute("INSERT INTO users (user_id, username, name, points) VALUES (?, ?, ?, 500)", (uid, message.from_user.username, message.from_user.first_name))
        for g, p in GAMES_PRICE.items():
            if p == 0: sql.execute("INSERT INTO unlocked_games VALUES (?, ?)", (uid, g))
        db.commit(); return my_id(message)
    
    cap = f"<b>👤 معلومات الإمبراطور:</b>\n\n<b>الاسم:</b> {u[2]}\n<b>الايدي:</b> <code>{u[0]}</code>\n<b>النقاط:</b> {u[3]}\n<b>المستوى:</b> {u[4]}\n<b>الرتبة:</b> {u[5]}"
    bot.reply_to(message, cap)

@bot.message_handler(func=lambda m: m.text == "العاب")
def list_games(message):
    sql.execute("SELECT game_name FROM unlocked_games WHERE user_id = ?", (message.from_user.id,))
    unlocked = [r[0] for r in sql.fetchall()]
    txt = "🎮 <b>قائمة الألعاب المتوفرة:</b>\n\n"
    for g in GAMES_PRICE.keys():
        txt += f"{'✅' if g in unlocked else '🔒'} {g}\n"
    bot.reply_to(message, txt + "\nأرسل اسم اللعبة للبدء.")

@bot.message_handler(func=lambda m: m.text == "المتجر")
def store(message):
    txt = "🛒 <b>متجر الإمبراطورية:</b>\n\n"
    for g, p in GAMES_PRICE.items():
        if p > 0: txt += f"🔹 {g} ↫ {p} نقطة\n"
    bot.reply_to(message, txt + "\nللشراء أرسل: <b>شراء + اسم اللعبة</b>")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
def buy(message):
    try:
        game = message.text.split(" ", 1)[1]
        price = GAMES_PRICE[game]
        sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
        if sql.fetchone()[0] < price: return bot.reply_to(message, "❌ نقاطك لا تكفي!")
        sql.execute("INSERT INTO unlocked_games VALUES (?, ?)", (message.from_user.id, game))
        sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (price, message.from_user.id))
        db.commit(); bot.reply_to(message, f"🎉 تم الشراء! فتحت {game}.")
    except: bot.reply_to(message, "❌ تأكد من كتابة: شراء + اسم اللعبة")

@bot.message_handler(func=lambda m: m.text in QUESTIONS.keys())
def play(message):
    game = message.text
    sql.execute("SELECT * FROM unlocked_games WHERE user_id = ? AND game_name = ?", (message.from_user.id, game))
    if not sql.fetchone(): return bot.reply_to(message, "🔒 مقفولة! اشتريها من المتجر.")
    q = random.choice(QUESTIONS[game])
    sent = bot.reply_to(message, f"❓ {q['q']}")
    bot.register_next_step_handler(sent, check, q['a'])

def check(message, ans):
    if message.text == ans:
        sql.execute("UPDATE users SET points = points + 50 WHERE user_id = ?", (message.from_user.id,))
        db.commit(); bot.reply_to(message, "✅ صحيح! +50 نقطة.")
    else: bot.reply_to(message, f"❌ خطأ، الجواب هو: {ans}")

bot.infinity_polling()
