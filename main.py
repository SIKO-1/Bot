import os, sqlite3, random, telebot
from telebot import types

# --- 1. الإعدادات والتوكن ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324  # ايديك كمطور

# --- 2. قاعدة البيانات المتطورة ---
db = sqlite3.connect("kira_final_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, 
    name TEXT, 
    points INTEGER DEFAULT 1000, 
    level INTEGER DEFAULT 1, 
    role TEXT DEFAULT 'عضو', 
    banned INTEGER DEFAULT 0)""")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

# --- 3. بنك الـ 200 سؤال (20 لعبة × 10 أسئلة) ---
GAMES_CONFIG = {
    "عواصم": {"p": 500, "r": "عادية ⚪"}, "رياضة": {"p": 550, "r": "عادية ⚪"}, "دين": {"p": 500, "r": "عادية ⚪"}, "ذكاء": {"p": 600, "r": "عادية ⚪"}, "تحدي": {"p": 500, "r": "عادية ⚪"},
    "أنمي": {"p": 1200, "r": "نادرة 🔵"}, "أفلام": {"p": 1300, "r": "نادرة 🔵"}, "تاريخ": {"p": 1100, "r": "نادرة 🔵"}, "جغرافيا": {"p": 1000, "r": "نادرة 🔵"}, "علوم": {"p": 1500, "r": "نادرة 🔵"},
    "برمجة": {"p": 2200, "r": "أسطورية 🔥"}, "فضاء": {"p": 2000, "r": "أسطورية 🔥"}, "حضارات": {"p": 2300, "r": "أسطورية 🔥"}, "سيارات": {"p": 2100, "r": "أسطورية 🔥"}, "طب": {"p": 2500, "r": "أسطورية 🔥"},
    "فلسفة": {"p": 5000, "r": "إمبراطورية 👑"}, "منطق": {"p": 5000, "r": "إمبراطورية 👑"}, "هكر": {"p": 5000, "r": "إمبراطورية 👑"}, "أساطير": {"p": 5000, "r": "إمبراطورية 👑"}, "الغاز_صعبة": {"p": 5000, "r": "إمبراطورية 👑"}
}

# توليد الأسئلة (سيتم استخدام الأزرار)
QUESTIONS = {g: [{"q": f"سؤال في {g} رقم {i}؟", "o": ["صح", "خطأ", "ربما"], "a": "صح"} for i in range(1, 11)] for g in GAMES_CONFIG.keys()}

# --- 4. فلاتر الحظر والمستوى ---
@bot.message_handler(func=lambda m: True)
def filter_all(message):
    sql.execute("SELECT banned FROM users WHERE user_id = ?", (message.from_user.id,))
    res = sql.fetchone()
    if res and res[0] == 1: return
    bot.continue_command_handling(message)

# --- 5. أوامر المطور والتحكم ---
@bot.message_handler(func=lambda m: m.text == "لوحة التحكم" and m.from_user.id == DEV_ID)
def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 الاحصائيات", callback_data="stats"),
        types.InlineKeyboardButton("🚫 حظر", callback_data="ban_user"),
        types.InlineKeyboardButton("✨ تعيين إمبراطور", callback_data="set_emp")
    )
    bot.reply_to(message, "🛠️ <b>لوحة تحكم الإمبراطور:</b>", reply_markup=markup)

@bot.message_handler(func=lambda m: m.reply_to_message and m.from_user.id == DEV_ID)
def dev_reply_actions(message):
    tid = message.reply_to_message.from_user.id
    if message.text.startswith("رفع "):
        pts = int(message.text.split()[1])
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (pts, tid))
        db.commit(); bot.reply_to(message, f"✅ تم شحن {pts} نقطة.")
    elif message.text == "حظر":
        sql.execute("UPDATE users SET banned = 1 WHERE user_id = ?", (tid,))
        db.commit(); bot.reply_to(message, "🚫 تم الحظر.")
    elif message.text == "امبراطور":
        sql.execute("UPDATE users SET role = 'الامبراطور ✨' WHERE user_id = ?", (tid,))
        db.commit(); bot.reply_to(message, "👑 تم التعيين.")

# --- 6. نظام المستوى المتضاعف ---
@bot.message_handler(func=lambda m: m.text == "المستوى")
def level_up_check(message):
    sql.execute("SELECT level, points FROM users WHERE user_id = ?", (message.from_user.id,))
    lv, pts = sql.fetchone()
    req = lv * 1500  # المتطلبات تتضاعف
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🆙 هل تريد رفع مستواك؟", callback_data=f"lvl_up|{req}"))
    bot.reply_to(message, f"⭐ <b>مستواك:</b> {lv}\n💰 <b>نقاطك:</b> {pts}\n🎯 <b>المطلوب للترقية:</b> {req}ن", reply_markup=markup)

# --- 7. المتجر والألعاب والأوامر العامة ---
@bot.message_handler(func=lambda m: m.text in ["ايدي", "ا"])
def get_info(message):
    uid = message.from_user.id
    sql.execute("INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)", (uid, message.from_user.first_name))
    sql.execute("SELECT points, level, role FROM users WHERE user_id = ?", (uid,))
    p, l, r = sql.fetchone()
    bot.reply_to(message, f"👤 <b>الاسم:</b> {message.from_user.first_name}\n💰 <b>النقاط:</b> {p}\n⭐ <b>المستوى:</b> {l}\n🏅 <b>الرتبة:</b> {r}")

@bot.message_handler(func=lambda m: m.text == "العاب")
def games_list(message):
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (message.from_user.id,))
    un = [r[0] for r in sql.fetchall()]
    txt = "🎮 <b>قائمة الألعاب (20 لعبة):</b>\n\n"
    for g, i in GAMES_CONFIG.items():
        s = "✅" if g in un else "🔒"
        txt += f"{s} {g} | {i['r']} | {i['p']}ن\n"
    bot.reply_to(message, txt + "\nأرسل اسم اللعبة للبدء.")

@bot.message_handler(func=lambda m: m.text == "المتجر")
def shop(message):
    txt = "🛒 <b>المتجر الإمبراطوري:</b>\n"
    for g, i in GAMES_CONFIG.items():
        txt += f"🔹 {g} ↫ {i['p']}ن\n"
    bot.reply_to(message, txt + "\nللشراء: شراء + اسم اللعبة")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
def buy_game(message):
    g = message.text.replace("شراء ", "").strip()
    if g not in GAMES_CONFIG: return
    sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
    if sql.fetchone()[0] < GAMES_CONFIG[g]['p']: return bot.reply_to(message, "❌ نقاطك لا تكفي.")
    sql.execute("INSERT INTO unlocked VALUES (?, ?)", (message.from_user.id, g))
    sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (GAMES_CONFIG[g]['p'], message.from_user.id))
    db.commit(); bot.reply_to(message, f"🎉 تم فتح {g}!")

# --- 8. معالجة العمليات (Callback) ---
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    uid = call.from_user.id
    if call.data.startswith("lvl_up|"):
        req = int(call.data.split("|")[1])
        sql.execute("SELECT points, level FROM users WHERE user_id = ?", (uid,))
        p, l = sql.fetchone()
        if p >= req:
            sql.execute("UPDATE users SET level = level + 1, points = points - ? WHERE user_id = ?", (req, uid))
            db.commit(); bot.edit_message_text(f"🎊 تم رفع مستواك إلى {l+1}!", call.message.chat.id, call.message.message_id)
        else: bot.answer_callback_query(call.id, f"❌ تحتاج {req-p}ن إضافية!", show_alert=True)
    
    elif call.data.startswith("game|"):
        _, ans, cor = call.data.split("|")
        if ans == cor:
            sql.execute("UPDATE users SET points = points + 50 WHERE user_id = ?", (uid,))
            db.commit(); bot.edit_message_text("✅ صح! +50ن", call.message.chat.id, call.message.message_id)
        else: bot.edit_message_text(f"❌ خطأ! الجواب: {cor}", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda m: m.text in GAMES_CONFIG.keys())
def start_game(message):
    g = message.text
    sql.execute("SELECT * FROM unlocked WHERE user_id = ? AND game = ?", (message.from_user.id, g))
    if not sql.fetchone(): return bot.reply_to(message, "🔒 اشتريها أولاً.")
    q = random.choice(QUESTIONS[g])
    m_up = types.InlineKeyboardMarkup()
    for o in q['o']: m_up.add(types.InlineKeyboardButton(o, callback_data=f"game|{o}|{q['a']}"))
    bot.send_message(message.chat.id, f"❓ {q['q']}", reply_markup=m_up)

# --- 9. حل مشكلة التعليق النهائي ---
bot.remove_webhook() # هذا السطر سينهي أي تعليق قديم فوراً
bot.infinity_polling(skip_pending=True)
