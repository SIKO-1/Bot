import os, sqlite3, telebot
from telebot import types
import games_system as gs  # ربط ملف الألعاب والأسعار

# --- الإعدادات والتوكن ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324  # ايديك الخاص كمطور

# --- قاعدة البيانات ---
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
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

# --- [ قائمة الأوامر ] ---
@bot.message_handler(func=lambda m: m.text in ["اوامر", "امر", "الأوامر"])
def cmd_list(message):
    txt = """📜 <b>قائمة أوامر الإمبراطورية:</b>
    
🎮 <b>العاب</b> ↫ عرض الألعاب المفتوحة والمقفلة
📊 <b>مستواي</b> ↫ عرض رتبتك ونقاطك
🛒 <b>المتجر</b> ↫ شراء ألعاب جديدة
🏰 <b>الامبراطورية</b> ↫ إدارة الدولة (للمطور)"""
    bot.reply_to(message, txt)

# --- [ نظام الإدارة واللوحة ] ---
@bot.message_handler(func=lambda m: m.text == "الامبراطورية")
def admin_panel(message):
    if message.from_user.id != DEV_ID:
        return bot.reply_to(message, "⚠️ خاص بالمؤسس فقط!")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 الاحصائيات", callback_data="st_stats"),
        types.InlineKeyboardButton("🚫 حظر عضو", callback_data="st_ban")
    )
    bot.reply_to(message, "🏰 <b>أهلاً بك في غرفة القيادة:</b>", reply_markup=markup)

@bot.message_handler(func=lambda m: m.reply_to_message and m.from_user.id == DEV_ID)
def dev_actions(message):
    tid = message.reply_to_message.from_user.id
    cmd = message.text
    
    if cmd.startswith("رفع رتبة "):
        role = cmd.replace("رفع رتبة ", "")
        sql.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, tid))
        bot.reply_to(message, f"🏅 تم منح العضو رتبة: {role}")
    elif cmd == "حظر":
        sql.execute("UPDATE users SET banned = 1 WHERE user_id = ?", (tid,))
        bot.reply_to(message, "🚫 تم نفيه من الإمبراطورية.")
    elif cmd.startswith("شحن "):
        pts = int(cmd.split()[1])
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (pts, tid))
        bot.reply_to(message, f"💰 تم إضافة {pts} نقطة.")
    db.commit()

# --- [ نظام الألعاب والربط ] ---
@bot.message_handler(func=lambda m: m.text == "العاب")
def show_games(message):
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (message.from_user.id,))
    un = [r[0] for r in sql.fetchall()]
    bot.reply_to(message, gs.get_games_menu(un))

@bot.message_handler(func=lambda m: m.text.startswith("شراء "))
def buy_game(message):
    g = message.text.replace("شراء ", "").strip()
    if g not in gs.GAMES_DATA: return
    
    sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
    pts = sql.fetchone()[0]
    price = gs.GAMES_DATA[g]['buy']
    
    if pts < price: return bot.reply_to(message, "❌ نقاطك لا تكفي!")
    
    sql.execute("INSERT INTO unlocked VALUES (?, ?)", (message.from_user.id, g))
    sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (price, message.from_user.id))
    db.commit(); bot.reply_to(message, f"✅ تم فتح <b>{g}</b>!")

@bot.message_handler(func=lambda m: m.text.startswith("بيع "))
def sell_game(message):
    g = message.text.replace("بيع ", "").strip()
    if g not in gs.GAMES_DATA or gs.GAMES_DATA[g]['sell'] == 0: return
    
    sql.execute("SELECT * FROM unlocked WHERE user_id = ? AND game = ?", (message.from_user.id, g))
    if not sql.fetchone(): return bot.reply_to(message, "❌ أنت لا تملك هذه اللعبة!")
    
    cash = gs.GAMES_DATA[g]['sell']
    sql.execute("DELETE FROM unlocked WHERE user_id = ? AND game = ?", (message.from_user.id, g))
    sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (cash, message.from_user.id))
    db.commit(); bot.reply_to(message, f"💰 تم بيع <b>{g}</b> مقابل {cash}ن.")

# --- [ تشغيل البوت وإصلاح التعليق ] ---
bot.remove_webhook()
print("✅ الإمبراطورية تعمل الآن...")
bot.infinity_polling(skip_pending=True)
