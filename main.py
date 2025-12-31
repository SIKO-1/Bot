import os, sqlite3, random, telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEVELOPER_ID = 5860391324 

# قاعدة بيانات نظيفة
db = sqlite3.connect("kira.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 1000, name TEXT)")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

GAMES = {
    "عواصم": {"p": 0, "q": "عاصمة العراق؟", "a": "بغداد"},
    "رياضة": {"p": 0, "q": "نادي لقب بالملكي؟", "a": "ريال مدريد"},
    "أنمي": {"p": 500, "q": "بطل ون بيس؟", "a": "لوفي"},
    "ذكاء": {"p": 0, "q": "خال أولاد عمتك؟", "a": "ابوك"}
}

@bot.message_handler(func=lambda m: m.text in ["ايدي", "ا"])
def my_id(message):
    uid = message.from_user.id
    sql.execute("INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)", (uid, message.from_user.first_name))
    sql.execute("SELECT points FROM users WHERE user_id = ?", (uid,))
    pts = sql.fetchone()[0]
    bot.reply_to(message, f"👤 <b>الاسم:</b> {message.from_user.first_name}\n💰 <b>نقاطك:</b> {pts}")

@bot.message_handler(func=lambda m: m.text == "العاب")
def all_g(message):
    txt = "🎮 <b>الألعاب:</b>\n"
    for g in GAMES.keys(): txt += f"🔹 {g}\n"
    bot.reply_to(message, txt + "\nأرسل اسم اللعبة للعب.")

@bot.message_handler(func=lambda m: m.text in GAMES.keys())
def play(message):
    g = message.text
    q = GAMES[g]
    m_s = bot.reply_to(message, f"❓ {q['q']}")
    bot.register_next_step_handler(m_s, check, q['a'])

def check(message, a):
    if message.text == a:
        sql.execute("UPDATE users SET points = points + 50 WHERE user_id = ?", (message.from_user.id,))
        db.commit()
        bot.reply_to(message, "✅ صح! +50 نقطة.")
    else: bot.reply_to(message, f"❌ خطأ، الجواب: {a}")

bot.infinity_polling()
