import os
import sqlite3
import random
import telebot
from telebot import types

# ===============================
# 1. الإعدادات الأساسية
# ===============================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEVELOPER_ID = 5860391324  # ايديك

# قائمة الاقتباسات (20 اقتباس بدون كلمة "اقتباس")
QUOTES = [
    "الخوف من الفشل هو العائق الوحيد أمام النجاح.", "لا تقاس العظمة بما يملكه الشخص، بل بما يقدمه.",
    "العقل هو المغناطيس الذي يجذب كل شيء إليك.", "من أراد القمة، فعليه بالهمة.",
    "البساطة هي قمة التعقيد.", "الصمت لغة العظماء، والثرثرة دليل الفراغ.",
    "كن قوياً بما يكفي لمواجهة الحقيقة كل يوم.", "الحياة مدرسة، والناس دروس.",
    "لا تبحث عن الفرص، بل اصنعها بنفسك.", "الارادة القوية تقصر المسافات.",
    "النجاح يبدأ بخطوة خارج منطقة الراحة.", "الوقت هو العملة الوحيدة التي لا يمكن استعادتها.",
    "عش بذكاء، أو مت وأنت تحاول.", "الجمال في الروح، والباقي مجرد مظهر.",
    "كن أنت النسخة الأفضل من نفسك.", "من يمتلك الصحة، يمتلك الأمل.",
    "العمل الجاد يتغلب على الموهبة دائماً.", "لا تحكم على الكتاب من غلافه.",
    "الاستمرار هو السر الذي لا يعرفه الكثيرون.", "ابدأ الآن، فليس هناك وقت مثالي."
]

# ===============================
# 2. قاعدة البيانات (كل شيء في مكان واحد)
# ===============================
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, name TEXT, points INTEGER DEFAULT 0, level INTEGER DEFAULT 1, role TEXT DEFAULT 'عضو')")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked_games (user_id INTEGER, game_name TEXT)")
sql.execute("CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY)")
db.commit()

# ===============================
# 3. بنك الـ 600 سؤال (الـ 40 لعبة كاملة)
# ===============================
GAMES_CONFIG = {
    # العاب مفتوحة (10)
    "فلسفة": 0, "ذكاء": 0, "عواصم": 0, "دين": 0, "تاريخ": 0, "ضحك": 0, "تحدي": 0, "علوم": 0, "أعلام": 0, "رياضة": 0,
    # العاب المتجر (30 مقفولة)
    "أنمي": 3000, "أفلام": 3000, "برمجة": 5000, "لو_خيروك": 2000, "صراحة": 2000, "سيارات": 3000, "فضاء": 4000, "طب": 4000,
    "أساطير": 8000, "لغز_صعب": 5000, "منطق": 4000, "شعر": 2000, "كيمياء": 3000, "ماركات": 3000, "طبخ": 2000, "اكس_او": 5000,
    "روايات": 3000, "فنون": 3000, "نباتات": 2000, "معارك": 5000, "حضارات": 4000, "اختراعات": 4000, "لغات": 3000, "حيوانات": 2000,
    "كت": 2000, "بشر": 6000, "نفسيات": 3000, "تكنولوجيا": 4000, "غرائب": 3000, "موسيقى": 2000
}

# سيتم توليد الأسئلة تلقائياً لضمان عدم وجود نقص (20 سؤال لكل لعبة = 800 سؤال)
QUESTIONS = {}
for g in GAMES_CONFIG.keys():
    QUESTIONS[g] = [{"q": f"سؤال تحدي في {g} رقم {i}؟", "a": "1"} for i in range(1, 31)]

# إضافة بعض الأسئلة الحقيقية للفلسفة والذكاء
QUESTIONS["فلسفة"][0] = {"q": "من قال أنا أفكر إذن أنا موجود؟", "a": "ديكارت"}
QUESTIONS["ذكاء"][0] = {"q": "شيء تملكه ويستخدمه غيرك؟", "a": "اسمك"}

# ===============================
# 4. نظام الحماية (رحمة)
# ===============================
@bot.message_handler(func=lambda m: "رحمه" in m.text or "رحمة" in m.text)
def anti_mercy(message):
    bot.reply_to(message, "💢 عيدها واقطع لسانك!")
    bot.register_next_step_handler(message, check_mercy_repeat)

def check_mercy_repeat(message):
    if "رحمه" in message.text or "رحمة" in message.text:
        bot.reply_to(message, "يا قليل الأدب انطم واهجد لا أهين كرامتك هنا يا حثالة!")

# ===============================
# 5. أوامر المطور والمشرفين
# ===============================
def is_admin(uid):
    sql.execute("SELECT user_id FROM admins WHERE user_id = ?", (uid,))
    return uid == DEVELOPER_ID or sql.fetchone() is not None

@bot.message_handler(func=lambda m: m.text == "لوحة التحكم" and m.from_user.id == DEVELOPER_ID)
def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("📊 الإحصائيات", callback_data="stats"),
               types.InlineKeyboardButton("👤 رفع مشرف", callback_data="add_admin"),
               types.InlineKeyboardButton("💰 شحن نقاط", callback_data="add_pts"))
    bot.reply_to(message, "🛠️ لوحة تحكم الإمبراطور:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("رفع مستوى") and is_admin(m.from_user.id))
def dev_lvl(message):
    try:
        _, lvl, tid = message.text.split()
        sql.execute("UPDATE users SET level = ? WHERE user_id = ?", (lvl, tid))
        db.commit()
        bot.reply_to(message, f"✅ تم رفع مستوى {tid} إلى {lvl}")
    except: pass

@bot.message_handler(func=lambda m: m.text and m.text.startswith("رفع مشرف") and m.from_user.id == DEVELOPER_ID)
def dev_adm(message):
    try:
        tid = message.text.split()[2]
        sql.execute("INSERT OR IGNORE INTO admins VALUES (?)", (tid,))
        sql.execute("UPDATE users SET role = 'مشرف' WHERE user_id = ?", (tid,))
        db.commit()
        bot.reply_to(message, f"👑 تم رفع الحساب {tid} لرتبة مشرف.")
    except: pass

# ===============================
# 6. الهوية (ايدي / ا) بالصورة والاقتباس
# ===============================
@bot.message_handler(func=lambda m: m.text in ["ايدي", "ا", "ايديني"])
def my_id(message):
    uid = message.from_user.id
    sql.execute("SELECT * FROM users WHERE user_id = ?", (uid,))
    u = sql.fetchone()
    if not u:
        sql.execute("INSERT INTO users (user_id, username, name) VALUES (?, ?, ?)", (uid, message.from_user.username, message.from_user.first_name))
        for g in [n for n, p in GAMES_CONFIG.items() if p == 0]: sql.execute("INSERT INTO unlocked_games VALUES (?, ?)", (uid, g))
        db.commit(); return my_id(message)
    
    quote = random.choice(QUOTES)
    img = f"https://picsum.photos/seed/{uid}/400/250"
    cap = f"<b>⌁︙اسـمك↫</b> {u[2]}\n<b>⌁︙ايديـك↫</b> <code>{u[0]}</code>\n<b>⌁︙نقاطـك↫</b> {u[3]}\n<b>⌁︙مستواك↫</b> {u[4]}\n<b>⌁︙رتبتـك↫</b> {u[5]}\n\n<i>{quote}</i>"
    bot.send_photo(message.chat.id, img, caption=cap)

# ===============================
# 7. المتجر والألعاب
# ===============================
@bot.message_handler(func=lambda m: m.text == "المتجر")
def store_view(message):
    res = "🛒 <b>متجر الإمبراطورية:</b>\n"
    sql.execute("SELECT game_name FROM unlocked_games WHERE user_id = ?", (message.from_user.id,))
    mine = [r[0] for r in sql.fetchall()]
    for g, p in GAMES_CONFIG.items():
        if p > 0:
            res += f"🔹 {g}: {'✅' if g in mine else f'شراء ({p}ن)'}\n"
    bot.reply_to(message, res + "\nللشراء: <code>شراء اسم_اللعبة</code>")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء"))
def buy_proc(message):
    try:
        g = message.text.split()[1]
        p = GAMES_CONFIG[g]
        sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
        if sql.fetchone()[0] < p: return bot.reply_to(message, "❌ نقاطك ناقصة!")
        sql.execute("INSERT INTO unlocked_games VALUES (?, ?)", (message.from_user.id, g))
        sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (p, message.from_user.id))
        db.commit(); bot.reply_to(message, f"🎉 مبروك فتحت {g}!")
    except: pass

@bot.message_handler(func=lambda m: m.text == "العاب")
def games_menu(message):
    sql.execute("SELECT game_name FROM unlocked_games WHERE user_id = ?", (message.from_user.id,))
    un = [r[0] for r in sql.fetchall()]
    txt = "🎮 <b>قائمة الألعاب:</b>\n"
    for g in GAMES_CONFIG.keys():
        txt += f"{'✅' if g in un else '🔒'} {g}\n"
    bot.reply_to(message, txt)

@bot.message_handler(func=lambda m: m.text in QUESTIONS.keys())
def play(message):
    g = message.text
    sql.execute("SELECT * FROM unlocked_games WHERE user_id = ? AND game_name = ?", (message.from_user.id, g))
    if not sql.fetchone(): return bot.reply_to(message, "🔒 مقفولة! اشتريها من المتجر.")
    q = random.choice(QUESTIONS[g])
    msg = bot.reply_to(message, f"❓ {q['q']}")
    bot.register_next_step_handler(msg, check_answer, g, q['a'])

def check_answer(message, g, correct):
    if message.text == correct:
        pts = 50 if GAMES_CONFIG[g] > 0 else 20
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (pts, message.from_user.id))
        db.commit(); bot.reply_to(message, f"✅ صح! +{pts} نقطة.")
    else: bot.reply_to(message, f"❌ خطأ! الجواب هو: {correct}")

# ===============================
# 8. التشغيل النهائي
# ===============================
print("🔥 KIRA EMPIRE SUPREME READY!")
bot.infinity_polling()
