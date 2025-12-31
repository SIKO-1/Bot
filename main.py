# ===============================
#  KIRA BOT - TeleBot Version
#  Developer: كرار
# ===============================

import os
import sqlite3
import telebot
from telebot import types

# ===============================
#  TOKEN (Railway Environment)
# ===============================
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN غير موجود في متغيرات البيئة")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ===============================
#  DEVELOPER ID
# ===============================
DEVELOPER_ID = 5860391324

# ===============================
#  DATABASE
# ===============================
db = sqlite3.connect("kira.db", check_same_thread=False)
sql = db.cursor()

sql.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    messages INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    banned INTEGER DEFAULT 0
)
""")
db.commit()

# ===============================
#  UTIL FUNCTIONS
# ===============================
def register_user(user):
    sql.execute("SELECT * FROM users WHERE user_id = ?", (user.id,))
    data = sql.fetchone()

    if data is None:
        sql.execute("""
        INSERT INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
        """, (user.id, user.username, user.first_name))
        db.commit()

def add_message(user_id):
    sql.execute("""
    UPDATE users SET messages = messages + 1 WHERE user_id = ?
    """, (user_id,))
    db.commit()

def get_user(user_id):
    sql.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return sql.fetchone()

# ===============================
#  START
# ===============================
@bot.message_handler(commands=["start"])
def start(message):
    register_user(message.from_user)
    bot.reply_to(
        message,
        "👋 أهلاً بك في <b>بوت كيرا</b>\n"
        "اكتب <code>اوامر</code> لعرض القائمة"
    )

# ===============================
#  TEXT HANDLER
# ===============================
@bot.message_handler(func=lambda m: True)
def text_handler(message):
    user = message.from_user
    register_user(user)
    add_message(user.id)

    text = message.text.strip()

    # ===========================
    #  ايدي / ا
    # ===========================
    if text in ["ا", "ايدي"]:
        data = get_user(user.id)

        if data is None:
            bot.reply_to(message, "⚠️ خطأ في جلب بياناتك")
            return

        _, _, name, msgs, points, level, banned = data

        reply = f"""
↫ دغيـرھَا لزڪـت بيـھَہّ 😡😕
-------------------------
⌁︙اسمـك↫ {name}
⌁︙ايديـك↫ <code>{user.id}</code>
⌁︙معرفـك↫ @{user.username if user.username else 'لا يوجد'}
⌁︙رتبتـك↫ عضو
⌁︙رسائلـك↫ {msgs}
⌁︙نقاطـك↫ {points}
⌁︙مستواك↫ {level}
"""
        bot.reply_to(message, reply)
        return

    # ===========================
    #  اوامر
    # ===========================
    if text == "اوامر":
        reply = """
↫ قائمة الأوامر:
-------------------------
⌁︙ايدي
⌁︙نقاطي
⌁︙مستواي
⌁︙العاب
⌁︙لوحة التحكم
"""
        bot.reply_to(message, reply)
        return

    # ===========================
    #  نقاطي
    # ===========================
    if text == "نقاطي":
        data = get_user(user.id)
        bot.reply_to(message, f"🎯 نقاطك: {data[4]}")
        return

    # ===========================
    #  مستواي
    # ===========================
    if text == "مستواي":
        data = get_user(user.id)
        bot.reply_to(message, f"⭐ مستواك: {data[5]}")
        return

    # ===========================
    #  العاب (قائمة فقط)
    # ===========================
    if text == "العاب":
        bot.reply_to(
            message,
            "🎮 الألعاب المتوفرة:\n"
            "- xo\n"
            "- quiz\n"
            "- صح_خطأ\n\n"
            "اكتب اسم اللعبة للتشغيل"
        )
        return

    # ===========================
    #  لوحة التحكم (للمطور فقط)
    # ===========================
    if text == "لوحة التحكم":
        if user.id != DEVELOPER_ID:
            bot.reply_to(message, "⛔ هذا الأمر للمطور فقط")
            return

        reply = """
🛠 لوحة تحكم المطور:
-------------------------
⌁︙حظر [ايدي]
⌁︙فك حظر [ايدي]
⌁︙حذف النقاط [ايدي]
"""
        bot.reply_to(message, reply)
        return

# ===============================
#  RUN
# ===============================
print("🤖 KIRA BOT is running...")
bot.infinity_polling()
