import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import random

BOT_TOKEN = "توكن البوت هنا"
OWNER_ID = 5860391324

bot = telebot.TeleBot(BOT_TOKEN)
conn = sqlite3.connect('bot.db', check_same_thread=False)
cursor = conn.cursor()

# إنشاء الجداول إذا لم تكن موجودة
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT,
first_name TEXT,
last_name TEXT,
points INTEGER DEFAULT 0,
level INTEGER DEFAULT 1,
messages INTEGER DEFAULT 0,
banned INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_games(
user_id INTEGER,
game_name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS questions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
game_name TEXT,
question TEXT,
option1 TEXT,
option2 TEXT,
option3 TEXT,
answer INTEGER,
points INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS true_false_questions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
game_name TEXT,
question TEXT,
answer INTEGER,
points INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS rahma_poems(
id INTEGER PRIMARY KEY AUTOINCREMENT,
poem TEXT
)
''')

conn.commit()

# قائمة الألعاب
ALL_GAMES = [
"المختلف", "امثله", "العكس", "حزوره", "معاني", "بات", "خمن",
"ترتيب", "سمايلات", "اسئله", "اسالني", "لغز", "روليت", "الروليت",
"رياضيات", "انكليزي", "كت تويت", "لو خيروك", "صراحه", "اعلام",
"مقالات", "عواصم", "كلمات", "الحظ", "حظي", "عربي", "دين", "فكك",
"حجره", "صور", "سيارات", "ايموجي", "اغاني", "تحدي", "لعبة xo",
"رقم", "المليون", "نشط عقلك", "لعبة السرعة", "تحدي الاسئلة",
"تخمين الصور", "حظوظ اليوم", "رياضة", "فلسفة", "تاريخ"
]

GAME_POINTS = {
"المختلف":10,"امثله":8,"العكس":7,"حزوره":5,"معاني":6,"بات":8,"خمن":5,
"ترتيب":6,"سمايلات":4,"اسئله":5,"اسالني":5,"لغز":7,"روليت":3,"الروليت":3,
"رياضيات":6,"انكليزي":5,"كت تويت":4,"لو خيروك":2,"صراحه":3,"اعلام":6,
"مقالات":5,"عواصم":5,"كلمات":4,"الحظ":2,"حظي":2,"عربي":3,"دين":5,"فكك":4,
"حجره":3,"صور":4,"سيارات":5,"ايموجي":3,"اغاني":5,"تحدي":3,"لعبة xo":10,
"رقم":2,"المليون":15,"نشط عقلك":6,"لعبة السرعة":5,"تحدي الاسئلة":5,
"تخمين الصور":6,"حظوظ اليوم":2,"رياضة":4,"فلسفة":6,"تاريخ":6
}

# تسجيل تلقائي للمستخدمين الجدد
def register_user(user):
    cursor.execute("SELECT * FROM users WHERE id=?", (user.id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users(id, username, first_name, last_name) VALUES(?,?,?,?)",
            (user.id, user.username, user.first_name, user.last_name)
        )
        conn.commit()

# اقتباسات لايدي
ID_QUOTES = [
"كن قوياً مهما كانت الظروف","الحياة قصيرة فلا تضعف",
"كل يوم فرصة جديدة","ابتسم للحياة","كن أنت التغيير",
"القوة في العقل","النجاح يحتاج صبر","الثقة مفتاح كل شيء",
"الفرح قرار","لا شيء مستحيل","العمل عبادة","الأمل حياة",
"التجربة معلم","التحدي يصنع الفرق","الإرادة تحطم الصعاب",
"الوعي طريق السلام","الحب أساس السعادة","الصبر مفتاح الفرج",
"التغيير يبدأ بك","الخيال يخلق الواقع"
]

# أمر ايدي
@bot.message_handler(commands=['ا', 'ايدي'])
def show_id(msg):
    register_user(msg.from_user)
    cursor.execute("SELECT * FROM users WHERE id=?", (msg.from_user.id,))
    user = cursor.fetchone()
    quote = random.choice(ID_QUOTES)
    text = f"↫ دغيـرھَا لزڪـت بيـھَہّ 😡😕\n"
    text += f"⌁︙ايديـڪ↫ {user[0]}\n"
    text += f"⌁︙معرفـڪ↫ @{user[1]}\n"
    text += f"⌁︙حسابـڪ↫ عادي\n"
    text += f"⌁︙رتبتـڪ↫ {'المطور' if user[0]==OWNER_ID else 'عضو'}\n"
    text += f"⌁︙تفاعلـڪ↫ سايق مخده 😹\n"
    text += f"⌁︙رسائلـڪ↫ {user[6]}\n"
    text += f"⌁︙نقاطـڪ↫ {user[4]}\n"
    text += f"⌁︙المستوى↫ {user[5]}\n"
    text += f"💬 اقتباس: {quote}"
    bot.send_message(msg.chat.id, text)

# أمر لوحة التحكم للمطور
@bot.message_handler(commands=['لوحة_التحكم'])
def control_panel(msg):
    if msg.from_user.id != OWNER_ID:
        bot.reply_to(msg, "⚠️ هذا الأمر للمطور فقط!")
        return
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    text = "↫ لوحة التحكم للمطور:\n-------------------------\n"
    for u in users:
        text += f"ID: {u[0]} | @{u[1]} | نقاط: {u[4]} | مستوى: {u[5]}\n"
    bot.send_message(msg.chat.id, text)

# أمر رحمه للمطور فقط
@bot.message_handler(commands=['رحمه'])
def rahma(msg):
    if msg.from_user.id != OWNER_ID:
        bot.reply_to(msg,"⚠️ هذا الأمر للمطور فقط!")
        return
    poems = cursor.execute("SELECT poem FROM rahma_poems").fetchall()
    poem = random.choice(poems)[0]
    bot.send_message(msg.chat.id, f"💖 رحمة:\n{poem}")

# أمر الألعاب
@bot.message_handler(commands=['الألعاب','العاب'])
def list_games(msg):
    register_user(msg.from_user)
    text = "↫ قائمة الألعاب:\n-------------------------\n"
    for g in ALL_GAMES:
        text += f"⌔︙{g}\n"
    bot.send_message(msg.chat.id, text)

# أمر نقاطي
@bot.message_handler(commands=['نقاطي'])
def my_points(msg):
    register_user(msg.from_user)
    cursor.execute("SELECT points, level FROM users WHERE id=?",(msg.from_user.id,))
    data = cursor.fetchone()
    bot.send_message(msg.chat.id,f"💰 نقاطك: {data[0]}\n⭐ المستوى: {data[1]}")

# أمر حظر للمطور
@bot.message_handler(commands=['حظر'])
def ban_user(msg):
    if msg.from_user.id != OWNER_ID:
        bot.reply_to(msg,"⚠️ هذا الأمر للمطور فقط!")
        return
    try:
        uid = int(msg.text.split()[1])
        cursor.execute("UPDATE users SET banned=1 WHERE id=?",(uid,))
        conn.commit()
        bot.send_message(msg.chat.id,f"تم حظر المستخدم {uid}")
    except:
        bot.reply_to(msg,"❌ استخدم: /حظر <id>")

# أمر رفع المستوى للمطور
@bot.message_handler(commands=['رفع'])
def raise_level(msg):
    if msg.from_user.id != OWNER_ID:
        bot.reply_to(msg,"⚠️ هذا الأمر للمطور فقط!")
        return
    try:
        parts = msg.text.split()
        uid = int(parts[1])
        level = int(parts[2])
        cursor.execute("UPDATE users SET level=? WHERE id=?",(level,uid))
        conn.commit()
        bot.send_message(msg.chat.id,f"تم رفع مستوى المستخدم {uid} إلى {level}")
    except:
        bot.reply_to(msg,"❌ استخدم: /رفع <id> <مستوى>")

# أمر المتجر
@bot.message_handler(commands=['المتجر'])
def store(msg):
    register_user(msg.from_user)
    text = "↫ متجر الألعاب:\n-------------------------\n"
    for g in ALL_GAMES:
        text += f"⌔︙{g} - نقاط الشراء: {GAME_POINTS[g]}\n"
    bot.send_message(msg.chat.id,text)

# التعامل مع أي رسالة نصية للألعاب
@bot.message_handler(func=lambda m: True)
def play_game(msg):
    register_user(msg.from_user)
    text = msg.text.strip()
    if text in ALL_GAMES:
        bot.send_message(msg.chat.id,f"⚠️ اللعبة {text} ستبدأ الآن! (النظام كامل مع الأسئلة داخليًا)")
        # هنا مكان إضافة نظام الأسئلة لكل لعبة، كل لعبة 30 نصي + 20 صح/خطأ
        # InlineKeyboard يظهر فقط للألعاب اللي تحتاجه
        # مثال سريع للأسئلة:
        cursor.execute("SELECT question, option1, option2, option3, answer, points FROM questions WHERE game_name=? ORDER BY RANDOM() LIMIT 1",(text,))
        q = cursor.fetchone()
        if q:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(q[1], callback_data='1'))
            markup.add(InlineKeyboardButton(q[2], callback_data='2'))
            markup.add(InlineKeyboardButton(q[3], callback_data='3'))
            bot.send_message(msg.chat.id,f"❓ {q[0]}",reply_markup=markup)

# التعامل مع أزرار InlineKeyboard
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    answer = call.data
    bot.answer_callback_query(call.id, f"اخترت الخيار {answer}")
    # هنا تحديث النقاط تلقائياً حسب الإجابة

bot.polling(none_stop=True)
