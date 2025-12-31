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
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, name TEXT, points INTEGER DEFAULT 1000, 
    level INTEGER DEFAULT 1, role TEXT DEFAULT 'عضو', banned INTEGER DEFAULT 0)""")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked (user_id INTEGER, game TEXT)")
db.commit()

# --- [ حماية الإمبراطورية ] ---
@bot.message_handler(func=lambda m: True, content_types=['text'])
def security_check(message):
    sql.execute("SELECT banned FROM users WHERE user_id = ?", (message.from_user.id,))
    res = sql.fetchone()
    if res and res[0] == 1: return
    bot.continue_command_handling(message)

# --- [ نظام المتجر والشراء ] ---
@bot.message_handler(func=lambda m: m.text == "المتجر")
def shop(message):
    bot.reply_to(message, "🛒 <b>مرحباً بك في المتجر!</b>\nللشراء أرسل: <code>شراء اسم اللعبة</code>\nللبيع أرسل: <code>بيع اسم اللعبة</code>\n\nمثال: <code>شراء أنمي</code>")

@bot.message_handler(func=lambda m: m.text.startswith("شراء "))
def buy_logic(message):
    game = message.text.replace("شراء ", "").strip()
    if game not in gs.GAMES_DATA: return bot.reply_to(message, "❌ هذه اللعبة غير موجودة.")
    
    sql.execute("SELECT points FROM users WHERE user_id = ?", (message.from_user.id,))
    pts = sql.fetchone()[0]
    price = gs.GAMES_DATA[game]['buy']
    
    if pts < price: return bot.reply_to(message, f"❌ نقاطك ({pts}) لا تكفي لشراء {game} بسعر {price}ن.")
    
    sql.execute("INSERT INTO unlocked VALUES (?, ?)", (message.from_user.id, game))
    sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (price, message.from_user.id))
    db.commit()
    bot.reply_to(message, f"✅ مبروك! تم فتح لعبة <b>{game}</b> بنجاح.")

# --- [ أوامر الإدارة والمطور ] ---
@bot.message_handler(func=lambda m: m.text == "الامبراطورية" and m.from_user.id == DEV_ID)
def admin_panel(message):
    bot.reply_to(message, "🏰 <b>لوحة تحكم الإمبراطور:</b>\n\n- <code>شحن [عدد]</code> (بالرد)\n- <code>حظر</code> (بالرد)\n- <code>الغاء حظر</code> (بالرد)\n- <code>رفع رتبة [الاسم]</code> (بالرد)")

@bot.message_handler(func=lambda m: m.reply_to_message and m.from_user.id == DEV_ID)
def admin_actions(message):
    tid = message.reply_to_message.from_user.id
    msg = message.text
    if msg.startswith("شحن "):
        val = int(msg.split()[1])
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (val, tid))
        bot.reply_to(message, f"💰 تم شحن {val} نقطة للعضو.")
    elif msg == "حظر":
        sql.execute("UPDATE users SET banned = 1 WHERE user_id = ?", (tid))
        bot.reply_to(message, "🚫 تم الحظر.")
    elif msg.startswith("رفع رتبة "):
        role = msg.replace("رفع رتبة ", "")
        sql.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, tid))
        bot.reply_to(message, f"🏅 تم الترقية إلى {role}.")
    db.commit()

# --- [ تشغيل الألعاب ] ---
@bot.message_handler(func=lambda m: m.text == "العاب")
def list_games(message):
    sql.execute("SELECT game FROM unlocked WHERE user_id = ?", (message.from_user.id,))
    un = [r[0] for r in sql.fetchall()]
    bot.reply_to(message, gs.get_games_menu(un))

@bot.message_handler(func=lambda m: m.text in gs.GAMES_DATA.keys())
def handle_game(message):
    # التحقق من ملكية اللعبة أو كونها مجانية
    sql.execute("SELECT * FROM unlocked WHERE user_id = ? AND game = ?", (message.from_user.id, message.text))
    if message.text not in gs.RANDOM_FREE_GAMES and not sql.fetchone():
        return bot.reply_to(message, "🔒 اللعبة مقفلة، اشتريها من المتجر أولاً.")
    gs.start_game_logic(bot, message, message.text)

bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
