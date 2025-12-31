import os, sqlite3, telebot
from telebot import types
import games_system as gs # ربط ملف الألعاب

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324 

# إعداد قاعدة البيانات
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 1000, role TEXT DEFAULT 'عضو')")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

# --- [ نظام المتجر والشراء ] ---
@bot.message_handler(func=lambda m: m.text == "المتجر")
def shop(message):
    bot.reply_to(message, "🛒 <b>متجر الإمبراطورية:</b>\nللشراء أرسل: <code>شراء اسم اللعبة</code>")

@bot.message_handler(func=lambda m: m.text.startswith("شراء "))
def buy_logic(message):
    game = message.text.replace("شراء ", "").strip()
    if game in gs.GAMES_DATA:
        price = gs.GAMES_DATA[game]['buy']
        sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
        if sql.fetchone()[0] >= price:
            sql.execute("INSERT INTO unlocked VALUES (?, ?)", (message.from_user.id, game))
            sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (price, message.from_user.id))
            db.commit(); bot.reply_to(message, f"✅ تم فتح {game}!")
        else: bot.reply_to(message, "❌ نقاطك لا تكفي.")

# --- [ أوامر المطور (بالرد) ] ---
@bot.message_handler(func=lambda m: m.reply_to_message and m.from_user.id == DEV_ID)
def admin_actions(message):
    tid = message.reply_to_message.from_user.id
    if message.text.startswith("شحن "):
        val = int(message.text.split()[1])
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (val, tid))
        bot.reply_to(message, f"💰 تم شحن {val} نقطة.")
    elif message.text.startswith("رفع رتبة "):
        role = message.text.replace("رفع رتبة ", "")
        sql.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, tid))
        bot.reply_to(message, f"🏅 تم منح رتبة {role}.")
    db.commit()

# --- [ تشغيل الألعاب ] ---
@bot.message_handler(func=lambda m: m.text == "العاب")
def games_list(message):
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (message.from_user.id,))
    un = [r[0] for r in sql.fetchall()]
    bot.reply_to(message, gs.get_games_menu(un))

@bot.message_handler(func=lambda m: m.text in gs.GAMES_DATA.keys())
def play_game(message):
    gs.start_game_logic(bot, message, message.text)

# معالجة الردود النصية
@bot.message_handler(func=lambda m: m.reply_to_message and "❓" in m.reply_to_message.text)
def handle_text(message):
    bot.reply_to(message, "✅ وصلت الإجابة! جاري التحقق من الصحة ومنح النقاط...")

bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
