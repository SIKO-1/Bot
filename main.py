import os, sqlite3, telebot
from telebot import types
import games_system as gs

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324 

# إعداد قاعدة البيانات
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, 
    points INTEGER DEFAULT 1000, 
    role TEXT DEFAULT 'عضو')""")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

# --- [ أوامر المطور - تصفير وشحن ] ---
@bot.message_handler(func=lambda m: m.reply_to_message and m.from_user.id == DEV_ID)
def admin_actions(message):
    tid = message.reply_to_message.from_user.id
    msg = message.text
    if msg.startswith("شحن "):
        val = int(msg.split()[1])
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (val, tid))
        bot.reply_to(message, f"💰 تم شحن {val} نقطة.")
    elif msg == "تصفير":
        sql.execute("UPDATE users SET points = 0 WHERE user_id = ?", (tid,))
        bot.reply_to(message, "🧹 تم تصفير نقاط العضو بالكامل.")
    db.commit()

# --- [ نظام المتجر والألعاب ] ---
@bot.message_handler(func=lambda m: m.text == "العاب")
def games_list(message):
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (message.from_user.id,))
    un = [r[0] for r in sql.fetchall()]
    bot.reply_to(message, gs.get_games_menu(un)) # الربط بملف الألعاب

@bot.message_handler(func=lambda m: m.text in gs.GAMES_DATA.keys())
def handle_game_play(message):
    # التحقق من الأقفال أو الألعاب المجانية
    sql.execute("SELECT * FROM unlocked WHERE user_id = ? AND game = ?", (message.from_user.id, message.text))
    if message.text not in gs.RANDOM_FREE_GAMES and not sql.fetchone():
        return bot.reply_to(message, "🔒 اللعبة مقفلة، اشتريها من المتجر.")
    gs.start_game_logic(bot, message, message.text)

# إزالة الدوال المسببة للأخطاء
bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
