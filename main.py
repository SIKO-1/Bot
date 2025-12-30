import os
import random
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")  # ضع توكن بوت كيرا هنا أو كمتغير بيئي
bot = telebot.TeleBot(TOKEN)

OWNER_ID = 5860391324  # كيرا (المطور)

# ================== قاعدة البيانات ==================
conn = sqlite3.connect("kira_bot.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    points INTEGER DEFAULT 0,
    money INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    messages INTEGER DEFAULT 0
)""")

c.execute("""CREATE TABLE IF NOT EXISTS user_games (
    user_id INTEGER,
    game_name TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY
)""")
conn.commit()

# ================== وظائف أساسية ==================
def get_user(user):
    c.execute("SELECT * FROM users WHERE id=?", (user.id,))
    row = c.fetchone()
    if not row:
        c.execute(
            "INSERT INTO users (id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
            (user.id, user.username, user.first_name, user.last_name)
        )
        conn.commit()
        return get_user(user)
    return row

def increment_messages(user_id):
    c.execute("UPDATE users SET messages=messages+1 WHERE id=?", (user_id,))
    conn.commit()

def get_user_games(user_id):
    c.execute("SELECT game_name FROM user_games WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    return [r[0] for r in rows]

def is_admin(uid):
    if uid == OWNER_ID:
        return True
    c.execute("SELECT * FROM admins WHERE id=?", (uid,))
    return bool(c.fetchone())

def add_points(user_id, pts):
    c.execute("UPDATE users SET points=points+?, money=money+? WHERE id=?", (pts, pts, user_id))
    c.execute("SELECT points FROM users WHERE id=?", (user_id,))
    points = c.fetchone()[0]
    level = min(999, points // 50 + 1)
    c.execute("UPDATE users SET level=? WHERE id=?", (level, user_id))
    conn.commit()

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    get_user(message.from_user)
    bot.send_message(message.chat.id, "👋 أهلًا بك في بوت كيرا الفخم!\nاكتب (اوامر) لعرض قائمة الأوامر")

# ================== أوامر ==================
@bot.message_handler(func=lambda m: m.text.lower() in ["اوامر", "الأوامر"])
def commands(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🎮 الألعاب", callback_data="games"))
    keyboard.add(InlineKeyboardButton("💰 نقاطي", callback_data="mypoints"))
    keyboard.add(InlineKeyboardButton("🆔 معلوماتي", callback_data="myid"))
    keyboard.add(InlineKeyboardButton("🛒 المتجر", callback_data="shop"))
    if message.from_user.id == OWNER_ID:
        keyboard.add(InlineKeyboardButton("🛠 لوحة التحكم", callback_data="dashboard"))
    bot.send_message(message.chat.id, "📜 قائمة الأوامر:", reply_markup=keyboard)

# ================== ايدي فخم ==================
@bot.callback_query_handler(func=lambda call: call.data=="myid")
def my_id(call):
    user = get_user(call.from_user)
    increment_messages(user[0])
    games = get_user_games(user[0])
    games_text = ", ".join(games) if games else "لا يوجد"
    photos = bot.get_user_profile_photos(user[0], limit=1)
    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        caption = f"""👤 {call.from_user.first_name} {call.from_user.last_name or ''}  
⭐ المستوى: {user[6]}  
🎯 النقاط: {user[4]}  
💰 الفلوس: {user[5]}  
🎮 الألعاب: {games_text}  
🆔 الايدي: {user[0]}  
📩 عدد الرسائل: {user[7]}"""
        bot.send_photo(call.message.chat.id, file_id, caption=caption)
    else:
        text = f"""👤 {call.from_user.first_name} {call.from_user.last_name or ''}  
⭐ المستوى: {user[6]}  
🎯 النقاط: {user[4]}  
💰 الفلوس: {user[5]}  
🎮 الألعاب: {games_text}  
🆔 الايدي: {user[0]}  
📩 عدد الرسائل: {user[7]}"""
        bot.send_message(call.message.chat.id, text)

# ================== الألعاب ==================
GAMES_LIST = [
    "المختلف", "الأمثلة", "العكس", "الحزورة", "المعاني", "البات",
    "التخمين", "ترتيب", "السمايلات", "أسئلة", "صح/خطأ", "لو خيروك",
    "صراحة", "إعلام", "مقالات", "عواصم", "كلمات", "الحظ", "حظي",
    "عربي", "دين", "فكك", "حجره", "صور", "سيارات", "ايموجي",
    "اغاني", "تحدي", "المليون", "نشط عقلك", "XO"
]

@bot.callback_query_handler(func=lambda call: call.data=="games")
def show_games(call):
    user_games = get_user_games(call.from_user.id)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for game in GAMES_LIST:
        label = f"{game} {'🔒' if game not in user_games else ''}"
        keyboard.add(InlineKeyboardButton(label, callback_data=f"game_{game}"))
    bot.send_message(call.message.chat.id, "🎮 قائمة الألعاب:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("game_"))
def start_game(call):
    game_name = call.data[5:]
    user_games = get_user_games(call.from_user.id)
    if game_name not in user_games:
        bot.answer_callback_query(call.id, "❌ هذه اللعبة مقفولة! افتحها أولاً")
        return
    if game_name == "XO":
        XO_start(call.from_user.id, call.message.chat.id)
    else:
        bot.send_message(call.message.chat.id, f"🎮 بدأت لعبة {game_name} (نظام نصي الآن)")

# ================== لعبة XO نصية ==================
XO_sessions = {}
def XO_start(user_id, chat_id):
    XO_sessions[user_id] = [" "]*9
    bot.send_message(chat_id, "🎮 XO ضد البوت\nاكتب رقم من 1 إلى 9 للعب:")

@bot.message_handler(func=lambda m: m.text.isdigit() and 1<=int(m.text)<=9)
def XO_move(message):
    if message.from_user.id not in XO_sessions:
        return
    board = XO_sessions[message.from_user.id]
    move = int(message.text)-1
    if board[move] != " ":
        bot.send_message(message.chat.id, "❌ الخانة مش فاضية!")
        return
    board[move] = "X"
    free = [i for i,v in enumerate(board) if v==" "]
    if free:
        board[random.choice(free)] = "O"
    bot.send_message(message.chat.id, draw_xo(board))

def draw_xo(board):
    return f"""
{board[0]} | {board[1]} | {board[2]}
---------
{board[3]} | {board[4]} | {board[5]}
---------
{board[6]} | {board[7]} | {board[8]}
"""

# ================== أوامر خاصة بالمطور ==================
@bot.message_handler(func=lambda m: m.text.lower() == "كرار")
def uncle_krar(message):
    bot.reply_to(message, "عمك 😎")

@bot.message_handler(func=lambda m: m.text.lower() == "رحمه")
def rahma_warn(message):
    bot.reply_to(message, "لو عدتها لاقص لسانك! 😡")

# ================== تتبع الرسائل ==================
@bot.message_handler(func=lambda m: True)
def track_messages(message):
    get_user(message.from_user)
    increment_messages(message.from_user.id)

print("🔥 BOT KIRA IS RUNNING 🔥")
bot.infinity_polling()
