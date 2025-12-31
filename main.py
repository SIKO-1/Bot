import os, sqlite3, random, telebot
from telebot import types

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324  # ايديك كمطور

# --- قاعدة البيانات ---
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT, points INTEGER DEFAULT 500)")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

# --- بنك الأسئلة (6 فئات) ---
QUESTIONS = {
    "عواصم": [{"q": "عاصمة العراق؟", "a": "بغداد"}, {"q": "عاصمة قطر؟", "a": "الدوحة"}, {"q": "عاصمة اليابان؟", "a": "طوكيو"}],
    "رياضة": [{"q": "نادي يلقب بالملكي؟", "a": "ريال مدريد"}, {"q": "بطل كأس العالم 2022؟", "a": "الارجنتين"}],
    "أنمي": [{"q": "بطل ون بيس؟", "a": "لوفي"}, {"q": "صاحب مفكرة الموت؟", "a": "لايت"}],
    "ذكاء": [{"q": "شيء يكتب ولا يقرأ؟", "a": "القلم"}, {"q": "خال أولاد عمتك؟", "a": "ابوك"}],
    "تاريخ": [{"q": "من فاتح القدس؟", "a": "صلاح الدين"}, {"q": "أين تقع الأهرامات؟", "a": "مصر"}],
    "إسلاميات": [{"q": "أول مؤذن في الإسلام؟", "a": "بلال"}, {"q": "أطول سورة؟", "a": "البقرة"}]
}

PRICES = {"عواصم": 0, "رياضة": 0, "ذكاء": 0, "إسلاميات": 0, "تاريخ": 0, "أنمي": 1000}

# --- أوامر المستخدم ---
@bot.message_handler(func=lambda m: m.text in ["ايدي", "ا"])
def my_id(message):
    uid = message.from_user.id
    sql.execute("INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)", (uid, message.from_user.first_name))
    sql.execute("SELECT points FROM users WHERE user_id = ?", (uid,))
    p = sql.fetchone()[0]
    bot.reply_to(message, f"👤 <b>الاسم:</b> {message.from_user.first_name}\n🆔 <b>الايدي:</b> <code>{uid}</code>\n💰 <b>نقاطك:</b> {p}")

@bot.message_handler(func=lambda m: m.text == "العاب")
def games(message):
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (message.from_user.id,))
    mine = [r[0] for r in sql.fetchall()]
    txt = "🎮 <b>ألعاب الإمبراطورية:</b>\n\n"
    for g, p in PRICES.items():
        status = "✅" if p == 0 or g in mine else "🔒"
        txt += f"{status} {g} {f'({p}ن)' if p > 0 else ''}\n"
    bot.reply_to(message, txt + "\nأرسل اسم اللعبة للبدء.")

@bot.message_handler(func=lambda m: m.text == "المتجر")
def store(message):
    txt = "🛒 <b>المتجر:</b>\n\n"
    for g, p in PRICES.items():
        if p > 0: txt += f"🔹 {g} ↫ {p} نقطة\n"
    bot.reply_to(message, txt + "\nللشراء أرسل: <b>شراء اسم اللعبة</b>")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
def buy(message):
    game = message.text.split(" ", 1)[1]
    if game not in PRICES or PRICES[game] == 0: return bot.reply_to(message, "❌ خطأ في الاسم.")
    sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
    if sql.fetchone()[0] < PRICES[game]: return bot.reply_to(message, "❌ نقاطك لا تكفي!")
    sql.execute("INSERT INTO unlocked VALUES (?, ?)", (message.from_user.id, game))
    sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (PRICES[game], message.from_user.id))
    db.commit(); bot.reply_to(message, f"🎉 مبروك! فتحت لعبة {game}.")

# --- نظام الألعاب ---
@bot.message_handler(func=lambda m: m.text in QUESTIONS.keys())
def play_game(message):
    g = message.text
    if PRICES[g] > 0:
        sql.execute("SELECT * FROM unlocked WHERE user_id = ? AND game = ?", (message.from_user.id, g))
        if not sql.fetchone(): return bot.reply_to(message, "🔒 اشتري اللعبة أولاً!")
    q = random.choice(QUESTIONS[g])
    m_s = bot.reply_to(message, f"❓ {q['q']}")
    bot.register_next_step_handler(m_s, check_a, q['a'])

def check_a(message, a):
    if message.text == a:
        sql.execute("UPDATE users SET points = points + 50 WHERE user_id = ?", (message.from_user.id,))
        db.commit(); bot.reply_to(message, "✅ صح! +50 نقطة.")
    else: bot.reply_to(message, f"❌ خطأ، الجواب: {a}")

# --- أوامر المطور ---
@bot.message_handler(func=lambda m: m.from_user.id == DEV_ID)
def dev_cmds(message):
    if message.text == "الاحصائيات":
        sql.execute("SELECT COUNT(*) FROM users")
        count = sql.fetchone()[0]
        bot.reply_to(message, f"📊 <b>عدد مستخدمي البوت:</b> {count}")
    elif message.text.startswith("رفع "): # مثال: رفع 5000 (يرد على رسالة الشخص)
        try:
            pts = int(message.text.split()[1])
            uid = message.reply_to_message.from_user.id
            sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (pts, uid))
            db.commit(); bot.reply_to(message, f"✅ تم إضافة {pts} نقطة للعضو.")
        except: bot.reply_to(message, "❌ رد على رسالة الشخص واكتب: رفع + العدد")

bot.infinity_polling(skip_pending=True)
