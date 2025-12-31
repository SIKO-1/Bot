import os
import sqlite3
import random
import telebot
from telebot import types

# ===============================
#  1. الإعدادات والتوكن
# ===============================
TOKEN = os.getenv("BOT_TOKEN") 
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEVELOPER_ID = 5860391324

# ===============================
#  2. قاعدة البيانات الملكية
# ===============================
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, username TEXT, name TEXT, 
    msgs INTEGER DEFAULT 0, points INTEGER DEFAULT 0, 
    level INTEGER DEFAULT 1, role TEXT DEFAULT 'عضو'
)""")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked_games (user_id INTEGER, game_name TEXT)")
db.commit()

# ===============================
#  3. الدوال المساعدة
# ===============================
def register_user(u):
    sql.execute("SELECT * FROM users WHERE user_id = ?", (u.id,))
    res = sql.fetchone()
    if res is None:
        sql.execute("INSERT INTO users (user_id, username, name) VALUES (?, ?, ?)", (u.id, u.username, u.first_name))
        db.commit()
        return register_user(u)
    return res

# ===============================
#  4. صلاحيات المطور المطلقة
# ===============================
@bot.message_handler(func=lambda m: m.from_user.id == DEVELOPER_ID)
def developer_powers(message):
    text = message.text
    
    # 1. إعطاء نقاط: (أضف نقاط [الايدي] [العدد])
    if text.startswith("أضف نقاط"):
        try:
            _, _, tid, amt = text.split()
            sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (amt, tid))
            db.commit()
            bot.reply_to(message, f"✅ تم إضافة {amt} نقطة للحساب {tid}")
        except: bot.reply_to(message, "الصيغة: أضف نقاط [الايدي] [العدد]")

    # 2. تصعيد مستوى: (رفع مستوى [الايدي] [المستوى])
    elif text.startswith("رفع مستوى"):
        try:
            _, _, tid, lv = text.split()
            sql.execute("UPDATE users SET level = ? WHERE user_id = ?", (lv, tid))
            db.commit()
            bot.reply_to(message, f"⭐ تم رفع مستوى {tid} إلى {lv}")
        except: bot.reply_to(message, "الصيغة: رفع مستوى [الايدي] [العدد]")

    # 3. فتح لعبة لشخص: (فتح [اسم اللعبة] [الايدي])
    elif text.startswith("فتح "):
        try:
            parts = text.split()
            game_name = parts[1]
            tid = parts[2]
            sql.execute("INSERT INTO unlocked_games (user_id, game_name) VALUES (?, ?)", (tid, game_name))
            db.commit()
            bot.reply_to(message, f"🔓 تم فتح لعبة {game_name} للمستخدم {tid}")
        except: bot.reply_to(message, "الصيغة: فتح [اسم_اللعبة] [الايدي]")

# ===============================
#  5. الأوامر العامة والايدي
# ===============================
@bot.message_handler(func=lambda m: m.text in ["ا", "ايدي"])
def my_id(message):
    u = register_user(message.from_user)
    reply = f"""
↫ دغيـرھَا لزڪـت بيـھَہّ 😡😕
-------------------------
⌁︙اسـمك↫ {u[2]}
⌁︙ايديـك↫ <code>{u[0]}</code>
⌁︙رتبتـك↫ {'المطور الملكي' if u[0] == DEVELOPER_ID else u[6]}
⌁︙نقاطـك↫ {u[4]}
⌁︙مستواك↫ {u[5]}
-------------------------
كن أنت التغيير الذي تطلبه.
"""
    try:
        photos = bot.get_user_profile_photos(u[0], limit=1)
        bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=reply)
    except: bot.reply_to(message, reply)

# ===============================
#  6. نظام تحويل النقاط (بموافقة المطور)
# ===============================
@bot.message_handler(func=lambda m: m.text and m.text.startswith("تحويل"))
def request_transfer(message):
    try:
        _, amount, tid = message.text.split()
        amount = int(amount)
        u = register_user(message.from_user)
        if u[4] < amount: return bot.reply_to(message, "❌ نقاطك غير كافية!")
        
        markup = types.InlineKeyboardMarkup()
        acc = types.InlineKeyboardButton("✅ قبول", callback_data=f"tr_acc_{u[0]}_{tid}_{amount}")
        rej = types.InlineKeyboardButton("❌ رفض", callback_data=f"tr_rej_{u[0]}")
        markup.add(acc, rej)
        
        bot.send_message(DEVELOPER_ID, f"🔔 <b>طلب تحويل:</b>\nمن: {u[0]}\nإلى: {tid}\nالمبلغ: {amount}", reply_markup=markup)
        bot.reply_to(message, "⏳ تم إرسال طلبك للمطور للموافقة.")
    except: bot.reply_to(message, "الصيغة: تحويل [النقاط] [الايدي]")

@bot.callback_query_handler(func=lambda call: call.data.startswith("tr_"))
def admin_decision(call):
    if call.from_user.id != DEVELOPER_ID: return
    p = call.data.split("_")
    if p[1] == "acc":
        sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (p[4], p[2]))
        sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (p[4], p[3]))
        db.commit()
        bot.edit_message_text("✅ تم قبول التحويل وتنفيذه.", call.message.chat.id, call.message.message_id)
        bot.send_message(p[2], "✅ وافق المطور على طلب التحويل الخاص بك.")
    else:
        bot.edit_message_text("❌ تم رفض التحويل.", call.message.chat.id, call.message.message_id)

# ===============================
#  7. حماية (رحمة) والقائمة
# ===============================
@bot.message_handler(func=lambda m: m.text == "اوامر")
def cmd_list(message):
    bot.reply_to(message, "📜 <b>قائمة الأوامر:</b>\n- ايدي\n- تحويل [نقاط] [ايدي]\n- متجر\n- العاب")

@bot.message_handler(func=lambda m: m.text and ("رحمه" in m.text or "رحمة" in m.text))
def protect(message):
    bot.reply_to(message, "عيدها واقطع لسانك! 😡")

# ===============================
#  8. التشغيل
# ===============================
print("🔥 KIRA CORE IS ONLINE")
bot.infinity_polling()
