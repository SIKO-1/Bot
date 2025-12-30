import os
import random
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

OWNER_ID = 5860391324

# ================== قاعدة البيانات ==================
conn = sqlite3.connect("bot.db", check_same_thread=False)
c = conn.cursor()

# إنشاء الجداول
c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    points INTEGER DEFAULT 0,
    money INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    rank TEXT DEFAULT 'عضو',
    messages INTEGER DEFAULT 0,
    bio TEXT DEFAULT 'وَاصْبِرْ فَإِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ'
)""")

c.execute("""CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY
)""")

c.execute("""CREATE TABLE IF NOT EXISTS user_games (
    user_id INTEGER,
    game_name TEXT
)""")

conn.commit()

# ================== الوظائف ==================
def get_user(user):
    c.execute("SELECT * FROM users WHERE id=?", (user.id,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO users (id, username) VALUES (?, ?)", (user.id, user.username))
        conn.commit()
        return get_user(user)
    return row

def add_points(user_id, pts):
    c.execute("UPDATE users SET points = points + ?, money = money + ? WHERE id=?", (pts, pts, user_id))
    c.execute("SELECT points FROM users WHERE id=?", (user_id,))
    points = c.fetchone()[0]
    level = min(999, points // 50 + 1)
    c.execute("UPDATE users SET level=? WHERE id=?", (level, user_id))
    conn.commit()

def is_admin(uid):
    if uid == OWNER_ID:
        return True
    c.execute("SELECT * FROM admins WHERE id=?", (uid,))
    return bool(c.fetchone())

# ================== أوامر لوحة التحكم ==================
@bot.message_handler(commands=["dashboard"])
def dashboard(message):
    if message.from_user.id != OWNER_ID:
        return
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("عرض المستخدمين", callback_data="show_users"))
    keyboard.add(InlineKeyboardButton("إضافة مشرف", callback_data="add_admin"))
    keyboard.add(InlineKeyboardButton("حذف مشرف", callback_data="remove_admin"))
    keyboard.add(InlineKeyboardButton("فتح لعبة", callback_data="open_game"))
    keyboard.add(InlineKeyboardButton("إغلاق لعبة", callback_data="close_game"))
    bot.send_message(message.chat.id, "📊 لوحة التحكم:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_dashboard(call):
    if call.message.chat.id != OWNER_ID:
        return
    if call.data == "show_users":
        c.execute("SELECT id, username, points, level FROM users")
        rows = c.fetchall()
        text = "👥 المستخدمين:\n"
        for r in rows:
            text += f"{r[0]} | @{r[1]} | نقاط: {r[2]} | مستوى: {r[3]}\n"
        bot.send_message(call.message.chat.id, text)
    elif call.data == "add_admin":
        bot.send_message(call.message.chat.id, "اكتب ايدي المشرف لإضافته: /addadmin ID")
    elif call.data == "remove_admin":
        bot.send_message(call.message.chat.id, "اكتب ايدي المشرف لحذفه: /deladmin ID")
    elif call.data == "open_game":
        bot.send_message(call.message.chat.id, "اكتب اسم اللعبة لفتحها: /open GAME")
    elif call.data == "close_game":
        bot.send_message(call.message.chat.id, "اكتب اسم اللعبة لإغلاقها: /close GAME")

# ================== إضافة / حذف مشرف ==================
@bot.message_handler(commands=["addadmin"])
def addadmin(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        uid = int(message.text.split()[1])
        c.execute("INSERT OR IGNORE INTO admins (id) VALUES (?)", (uid,))
        conn.commit()
        bot.reply_to(message, "✅ تم إضافة مشرف")
    except:
        bot.reply_to(message, "❌ صيغة خاطئة: /addadmin ID")

@bot.message_handler(commands=["deladmin"])
def deladmin(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        uid = int(message.text.split()[1])
        c.execute("DELETE FROM admins WHERE id=?", (uid,))
        conn.commit()
        bot.reply_to(message, "✅ تم حذف المشرف")
    except:
        bot.reply_to(message, "❌ صيغة خاطئة: /deladmin ID")

# ================== حذف نقاط ==================
@bot.message_handler(commands=["reset_points"])
def reset_points(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ أنت مو مصرح لك")
        return
    try:
        uid = int(message.text.split()[1])
        c.execute("UPDATE users SET points=0 WHERE id=?", (uid,))
        conn.commit()
        bot.reply_to(message, "✅ تم حذف النقاط")
    except:
        bot.reply_to(message, "❌ الصيغة: /reset_points ID")

# ================== امر رحمة سري ==================
love_texts = [
    "رحمه… كأن الله حين خلقك كان يبتسم.",
    "رحمه، مو اسم… هذا دعاء مستجاب.",
    "رحمه بالعقل وطن، وبالقلب فوضى جميلة.",
    "رحمه؟ هاي مو بشر… هاي أمان.",
    "رحمه، إذا ضحكت ينسى الحزن اسمه.",
    "رحمه تشبه السلام لما يتعب الإنسان."
]

@bot.message_handler(func=lambda m: m.text.lower() == "رحمه")
def rahma(message):
    text = random.choice(love_texts)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("المزيد 🤍", callback_data="more_love"))
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "more_love")
def more_love(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, random.choice(love_texts))

# ================== أمر ايدي ==================
@bot.message_handler(func=lambda m: m.text.lower() in ["ا", "ايدي"])
def my_id(message):
    c.execute("SELECT * FROM users WHERE id=?", (message.from_user.id,))
    u = c.fetchone()
    text = f"""↫ دغيـرھَا لزڪـت بيـھَہّ 😡😕

⌁︙ايديـڪ↫ {u[0]}
⌁︙معرفـڪ↫ @{u[1] if u[1] else 'غير محدد'}
⌁︙حسابـڪ↫ عادي
⌁︙رتبتـڪ↫ {u[5]}
⌁︙تفاعلـڪ↫ سايق مخده 😹
⌁︙رسائلـڪ↫ {u[6]}
⌁︙نقاطـڪ↫ {u[2]}
⌁︙البـايـــو↫ {u[7]}
"""
    bot.send_message(message.chat.id, text)

# ================== نظام ألعاب بسيط ==================
XO_games = {}

def draw_xo(board):
    return f"""
{board[0]} | {board[1]} | {board[2]}
---------
{board[3]} | {board[4]} | {board[5]}
---------
{board[6]} | {board[7]} | {board[8]}
"""

@bot.message_handler(func=lambda m: m.text.lower() == "xo")
def xo_start(message):
    XO_games[message.from_user.id] = [" "]*9
    bot.send_message(message.chat.id, "🎮 XO ضد البوت\nاكتب رقم من 1 إلى 9")

@bot.message_handler(func=lambda m: m.text.isdigit() and 1 <= int(m.text) <= 9)
def xo_move(message):
    if message.from_user.id not in XO_games:
        return
    board = XO_games[message.from_user.id]
    move = int(message.text)-1
    if board[move] != " ":
        return
    board[move] = "X"
    free = [i for i,v in enumerate(board) if v==" "]
    if free:
        board[random.choice(free)] = "O"
    bot.send_message(message.chat.id, draw_xo(board))

# ================== تشغيل البوت ==================
print("🔥 BOT IS RUNNING 🔥")
bot.infinity_polling()
