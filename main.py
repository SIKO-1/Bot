import os, sqlite3, telebot
from telebot import types
import games_system as gs  # الربط بملف الألعاب

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324 

# --- قاعدة البيانات ---
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, name TEXT, points INTEGER DEFAULT 1000, 
    level INTEGER DEFAULT 1, role TEXT DEFAULT 'عضو', banned INTEGER DEFAULT 0)""")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

# --- ميزة الألعاب المفتوحة تلقائياً ---
FREE_GAMES = ["عواصم", "رياضة", "دين", "ذكاء", "تحدي"]

# --- [ أوامر المستخدم ] ---
@bot.message_handler(func=lambda m: m.text in ["اوامر", "امر"])
def cmd_list(message):
    bot.reply_to(message, "📜 <b>أوامر الإمبراطورية:</b>\n\n🎮 <b>العاب</b> | 📊 <b>مستواي</b>\n🛒 <b>المتجر</b> | 🏰 <b>الامبراطورية</b>")

@bot.message_handler(func=lambda m: m.text == "مستواي")
def my_level(message):
    sql.execute("SELECT level, points, role FROM users WHERE user_id = ?", (message.from_user.id,))
    l, p, r = sql.fetchone()
    req = l * 2000 # متطلبات رفع المستوى
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"🆙 رفع المستوى ({req}ن)", callback_data=f"up_lv|{req}"))
    bot.reply_to(message, f"👤 <b>الرتبة:</b> {r}\n⭐ <b>المستوى:</b> {l}\n💰 <b>النقاط:</b> {p}", reply_markup=markup)

# --- [ إدارة الإمبراطورية - المطور ] ---
@bot.message_handler(func=lambda m: m.text == "الامبراطورية" and m.from_user.id == DEV_ID)
def admin_room(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🚫 حظر", callback_data="adm_ban"),
               types.InlineKeyboardButton("🏅 الرتب", callback_data="adm_role"),
               types.InlineKeyboardButton("💰 شحن", callback_data="adm_points"))
    bot.reply_to(message, "🏰 <b>غرفة القيادة:</b>\nاستخدم الرد على رسالة الشخص مع الأوامر التالية:\n- <code>رفع رتبة [الاسم]</code>\n- <code>شحن [عدد]</code>\n- <code>رفع مستوى [عدد]</code>", reply_markup=markup)

@bot.message_handler(func=lambda m: m.reply_to_message and m.from_user.id == DEV_ID)
def dev_actions(message):
    tid = message.reply_to_message.from_user.id
    msg = message.text
    if msg.startswith("رفع رتبة "):
        r = msg.replace("رفع رتبة ", ""); sql.execute("UPDATE users SET role = ? WHERE user_id = ?", (r, tid))
        bot.reply_to(message, f"🏅 تم منح رتبة {r}")
    elif msg.startswith("شحن "):
        p = int(msg.split()[1]); sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (p, tid))
        bot.reply_to(message, f"💰 تم شحن {p} نقطة")
    elif msg.startswith("رفع مستوى "):
        v = int(msg.split()[1]); sql.execute("UPDATE users SET level = level + ? WHERE user_id = ?", (v, tid))
        bot.reply_to(message, f"🆙 تم رفع المستوى بمقدار {v}")
    db.commit()

# --- [ تشغيل الألعاب والربط ] ---
@bot.message_handler(func=lambda m: m.text == "العاب")
def games_list(message):
    uid = message.from_user.id
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (uid,))
    un = [r[0] for r in sql.fetchall()] + FREE_GAMES
    bot.reply_to(message, gs.get_games_menu(un)) # استدعاء الزخرفة من الملف الثاني

@bot.message_handler(func=lambda m: m.text in gs.GAMES_DATA.keys())
def play_game(message):
    uid = message.from_user.id
    g_name = message.text
    sql.execute("SELECT * FROM unlocked WHERE user_id = ? AND game = ?", (uid, g_name))
    if g_name not in FREE_GAMES and not sql.fetchone():
        return bot.reply_to(message, "🔒 هذه اللعبة مقفلة! اشتريها من المتجر.")
    
    # تشغيل منطق اللعبة من الملف الثاني
    gs.start_game_logic(bot, message, g_name)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ans|"))
def handle_game_answers(call):
    _, ans, cor = call.data.split("|")
    if ans == cor:
        sql.execute("UPDATE users SET points = points + 50 WHERE user_id = ?", (call.from_user.id,))
        db.commit(); bot.edit_message_text(f"✅ كفو! إجابة صحيحة (+50ن)", call.message.chat.id, call.message.message_id)
    else: bot.edit_message_text(f"❌ خطأ! الجواب الصحيح: {cor}", call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("up_lv|"))
def level_up_callback(call):
    req = int(call.data.split("|")[1])
    sql.execute("SELECT points FROM users WHERE user_id = ?", (call.from_user.id,))
    if sql.fetchone()[0] >= req:
        sql.execute("UPDATE users SET level = level + 1, points = points - ? WHERE user_id = ?", (req, call.from_user.id))
        db.commit(); bot.answer_callback_query(call.id, "🎊 مبروك! تم رفع مستواك", show_alert=True)
    else: bot.answer_callback_query(call.id, "❌ نقاطك غير كافية!", show_alert=True)

bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
