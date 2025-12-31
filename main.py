import os, sqlite3, telebot
from telebot import types
import games_system as gs

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324 

# --- قاعدة البيانات ---
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 1000, role TEXT DEFAULT 'عضو')")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

# --- [ أوامر المتجر ] ---
@bot.message_handler(func=lambda m: m.text == "المتجر")
def shop(message):
    bot.reply_to(message, "🛒 <b>متجر الإمبراطورية:</b>\nلشراء لعبة أرسل: <code>شراء اسم اللعبة</code>")

@bot.message_handler(func=lambda m: m.text.startswith("شراء "))
def buy_logic(message):
    game = message.text.replace("شراء ", "").strip()
    if game in gs.GAMES_DATA:
        price = gs.GAMES_DATA[game]['buy']
        sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
        current_pts = sql.fetchone()[0]
        if current_pts >= price:
            sql.execute("INSERT INTO unlocked VALUES (?, ?)", (message.from_user.id, game))
            sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (price, message.from_user.id))
            db.commit()
            bot.reply_to(message, f"✅ مبروك! تم فتح لعبة <b>{game}</b>.")
        else: bot.reply_to(message, "❌ نقاطك لا تكفي!")

# --- [ أوامر المطور - بالرد ] ---
@bot.message_handler(func=lambda m: m.reply_to_message and m.from_user.id == DEV_ID)
def admin_actions(message):
    tid = message.reply_to_message.from_user.id
    msg = message.text
    if msg.startswith("شحن "):
        val = int(msg.split()[1])
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (val, tid))
        bot.reply_to(message, f"💰 تم شحن {val} نقطة للعضو.")
    elif msg == "تصفير":
        sql.execute("UPDATE users SET points = 0 WHERE user_id = ?", (tid,))
        bot.reply_to(message, "🧹 تم تصفير نقاط العضو بالكامل.")
    elif msg.startswith("رفع رتبة "):
        role = msg.replace("رفع رتبة ", "")
        sql.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, tid))
        bot.reply_to(message, f"🏅 تم ترقية العضو إلى: {role}")
    db.commit()

# --- [ نظام الألعاب ] ---
@bot.message_handler(func=lambda m: m.text == "العاب")
def games_list(message):
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (message.from_user.id,))
    un = [r[0] for r in sql.fetchall()]
    bot.reply_to(message, gs.get_games_menu(un))

@bot.message_handler(func=lambda m: m.text in gs.GAMES_DATA.keys())
def play_game(message):
    sql.execute("SELECT * FROM unlocked WHERE user_id = ? AND game = ?", (message.from_user.id, message.text))
    if message.text not in gs.RANDOM_FREE_GAMES and not sql.fetchone():
        return bot.reply_to(message, "🔒 هذه اللعبة مقفلة، اشتريها من المتجر.")
    gs.start_game_logic(bot, message, message.text)

# معالجة الإجابات الصحيحة (Callback)
@bot.callback_query_handler(func=lambda call: call.data.startswith("ans|"))
def handle_ans(call):
    _, ans, cor, reward = call.data.split("|")
    if ans == cor:
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (int(reward), call.from_user.id))
        db.commit()
        bot.edit_message_text(f"✅ صح! ربحت {reward}ن.", call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text(f"❌ خطأ! الجواب: {cor}", call.message.chat.id, call.message.message_id)

bot.infinity_polling(skip_pending=True)
