import os, sqlite3, random, telebot
from telebot import types

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324  # ايديك كمطور

# --- قاعدة البيانات ---
db = sqlite3.connect("kira_empire_final.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT, points INTEGER DEFAULT 500, level INTEGER DEFAULT 1, role TEXT DEFAULT 'عضو', banned INTEGER DEFAULT 0)")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

# --- البيانات والألعاب (20 لعبة × 10 أسئلة = 200 سؤال) ---
GAMES_CONFIG = {
    # عادية (500-600)
    "عواصم": {"p": 500, "r": "عادية ⚪"}, "رياضة": {"p": 550, "r": "عادية ⚪"}, "دين": {"p": 500, "r": "عادية ⚪"}, "ذكاء": {"p": 600, "r": "عادية ⚪"}, "تحدي": {"p": 500, "r": "عادية ⚪"},
    # نادرة (1000-1500)
    "أنمي": {"p": 1200, "r": "نادرة 🔵"}, "أفلام": {"p": 1300, "r": "نادرة 🔵"}, "تاريخ": {"p": 1100, "r": "نادرة 🔵"}, "جغرافيا": {"p": 1000, "r": "نادرة 🔵"}, "علوم": {"p": 1500, "r": "نادرة 🔵"},
    # أسطورية (2000-2500)
    "برمجة": {"p": 2200, "r": "أسطورية 🔥"}, "فضاء": {"p": 2000, "r": "أسطورية 🔥"}, "حضارات": {"p": 2300, "r": "أسطورية 🔥"}, "سيارات": {"p": 2100, "r": "أسطورية 🔥"}, "طب": {"p": 2500, "r": "أسطورية 🔥"},
    # إمبراطورية (5000)
    "فلسفة": {"p": 5000, "r": "إمبراطورية 👑"}, "منطق": {"p": 5000, "r": "إمبراطورية 👑"}, "هكر": {"p": 5000, "r": "إمبراطورية 👑"}, "أساطير": {"p": 5000, "r": "إمبراطورية 👑"}, "الغاز_صعبة": {"p": 5000, "r": "إمبراطورية 👑"}
}

# بنك الـ 200 سؤال (مثال مكرر للهيكل، يمكنك تعبئة الأجوبة الحقيقية)
QUESTIONS = {}
for g in GAMES_CONFIG.keys():
    QUESTIONS[g] = [{"q": f"سؤال في {g} رقم {i}؟", "o": ["صح", "خطأ", "ربما"], "a": "صح"} for i in range(1, 11)]

# --- نظام الحماية ---
@bot.message_handler(func=lambda m: True)
def check_ban(message):
    sql.execute("SELECT banned FROM users WHERE user_id = ?", (message.from_user.id,))
    res = sql.fetchone()
    if res and res[0] == 1: return # العضو محظور
    bot.continue_command_handling(message)

# --- لوحة المطور ---
@bot.message_handler(func=lambda m: m.text == "لوحة التحكم" and m.from_user.id == DEV_ID)
def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 إحصائيات", callback_data="dev_stats"),
        types.InlineKeyboardButton("🚫 حظر", callback_data="dev_ban"),
        types.InlineKeyboardButton("✨ تعيين إمبراطور", callback_data="dev_set_emp")
    )
    bot.reply_to(message, "🛠️ <b>لوحة تحكم الإمبراطور:</b>", reply_markup=markup)

# --- نظام المستوى ---
def get_lv_req(lv): return lv * 1000

@bot.message_handler(func=lambda m: m.text == "المستوى")
def lv_info(message):
    sql.execute("SELECT level, points FROM users WHERE user_id = ?", (message.from_user.id,))
    lv, pts = sql.fetchone()
    req = get_lv_req(lv)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🆙 رفع المستوى", callback_data="up_lv"))
    bot.reply_to(message, f"📊 <b>مستواك الحالي:</b> {lv}\n💰 <b>نقاطك:</b> {pts}\n🎯 <b>المطلوب للترفيع:</b> {req} نقطة", reply_markup=markup)

# --- أوامر المستخدم ---
@bot.message_handler(func=lambda m: m.text in ["ايدي", "ا"])
def my_id(message):
    uid = message.from_user.id
    sql.execute("INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)", (uid, message.from_user.first_name))
    sql.execute("SELECT points, level, role FROM users WHERE user_id = ?", (uid,))
    pts, lv, role = sql.fetchone()
    bot.reply_to(message, f"👤 <b>الاسم:</b> {message.from_user.first_name}\n<b>💰 النقاط:</b> {pts}\n<b>⭐ المستوى:</b> {lv}\n<b>🏅 الرتبة:</b> {role}\n<b>🆔 الايدي:</b> <code>{uid}</code>")

@bot.message_handler(func=lambda m: m.text == "العاب")
def games_menu(message):
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (message.from_user.id,))
    un = [r[0] for r in sql.fetchall()]
    txt = "🎮 <b>قائمة الألعاب:</b>\n"
    for g, i in GAMES_CONFIG.items():
        status = "✅" if g in un else "🔒"
        txt += f"{status} {g} | {i['r']} | {i['p']}ن\n"
    bot.reply_to(message, txt + "\nأرسل اسم اللعبة للبدء.")

@bot.message_handler(func=lambda m: m.text == "المتجر")
def store_menu(message):
    txt = "🛒 <b>المتجر الملكي:</b>\n"
    for g, i in GAMES_CONFIG.items():
        txt += f"💎 {g} ↫ {i['p']}ن\n"
    bot.reply_to(message, txt + "\nللشراء: <b>شراء اسم اللعبة</b>")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
def buy(message):
    g = message.text.replace("شراء ", "").strip()
    if g not in GAMES_CONFIG: return
    sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
    if sql.fetchone()[0] < GAMES_CONFIG[g]['p']: return bot.reply_to(message, "❌ نقاطك ناقصة!")
    sql.execute("INSERT OR IGNORE INTO unlocked VALUES (?, ?)", (message.from_user.id, g))
    sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (GAMES_CONFIG[g]['p'], message.from_user.id))
    db.commit(); bot.reply_to(message, f"🎉 تم فتح {g} بنجاح!")

# --- معالجة Callback الأزرار ---
@bot.callback_query_handler(func=lambda call: True)
def handle_calls(call):
    uid = call.from_user.id
    if call.data == "up_lv":
        sql.execute("SELECT level, points FROM users WHERE user_id = ?", (uid,))
        lv, pts = sql.fetchone()
        req = get_lv_req(lv)
        if pts >= req:
            sql.execute("UPDATE users SET level = level + 1, points = points - ? WHERE user_id = ?", (req, uid))
            db.commit()
            bot.answer_callback_query(call.id, "🎉 مبروك! تم رفع مستواك")
            bot.send_message(call.message.chat.id, f"🎊 تهانينا {call.from_user.first_name}! وصلت للمستوى {lv + 1}")
        else:
            bot.answer_callback_query(call.id, f"❌ تحتاج {req - pts} نقطة إضافية!", show_alert=True)
            
    elif call.data.startswith("game|"):
        _, user_ans, correct = call.data.split("|")
        if user_ans == correct:
            sql.execute("UPDATE users SET points = points + 50 WHERE user_id = ?", (uid))
            db.commit(); bot.edit_message_text(f"✅ صح! +50 نقطة", call.message.chat.id, call.message.message_id)
        else: bot.edit_message_text(f"❌ خطأ! الجواب: {correct}", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda m: m.text in GAMES_CONFIG.keys())
def play(message):
    g = message.text
    sql.execute("SELECT * FROM unlocked WHERE user_id = ? AND game = ?", (message.from_user.id, g))
    if not sql.fetchone(): return bot.reply_to(message, "🔒 اشتريها أولاً!")
    q_data = random.choice(QUESTIONS[g])
    markup = types.InlineKeyboardMarkup()
    for o in q_data['o']: markup.add(types.InlineKeyboardButton(o, callback_data=f"game|{o}|{q_data['a']}"))
    bot.send_message(message.chat.id, f"<b>❓ {q_data['q']}</b>", reply_markup=markup)

# أوامر المطور السريعة (رد على الشخص)
@bot.message_handler(func=lambda m: m.from_user.id == DEV_ID and m.reply_to_message)
def dev_actions(message):
    tid = message.reply_to_message.from_user.id
    if message.text == "حظر":
        sql.execute("UPDATE users SET banned = 1 WHERE user_id = ?", (tid,))
        db.commit(); bot.reply_to(message, "🚫 تم حظره نهائياً.")
    elif message.text == "امبراطور":
        sql.execute("UPDATE users SET role = 'الامبراطور ✨' WHERE user_id = ?", (tid,))
        db.commit(); bot.reply_to(message, "👑 تم تنصيبه كإمبراطور للدولة!")

bot.infinity_polling(skip_pending=True)
