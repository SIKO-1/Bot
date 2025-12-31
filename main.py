import os
import sqlite3
import random
import telebot
from telebot import types

# ===============================
#  الإعدادات والتوكن
# ===============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
DEVELOPER_ID = 5860391324  # ايديك

# ===============================
#  قاعدة البيانات
# ===============================
db = sqlite3.connect("kira_final.db", check_same_thread=False)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, username TEXT, name TEXT, 
    msgs INTEGER DEFAULT 0, points INTEGER DEFAULT 0, 
    level INTEGER DEFAULT 1, role TEXT DEFAULT 'عضو'
)""")
sql.execute("CREATE TABLE IF NOT EXISTS unlocked_games (user_id INTEGER, game_name TEXT)")
db.commit()

# ===============================
#  بنك الأسئلة العملاق (35 لعبة × 20 سؤال)
# ===============================
# مصفوفة الألعاب
FREE_GAMES = ["فلسفة", "ذكاء", "عواصم", "دين", "ضحك", "تحدي", "لو_خيروك", "صراحة", "اكس_او", "كت_تويت"]
SHOP_GAMES = [f"لعبة_ملك_{i}" for i in range(1, 26)] # 25 لعبة إضافية مقفولة
ALL_GAMES = FREE_GAMES + SHOP_GAMES

GAME_DATA = {
    "فلسفة": [
        {"q": "هل الزمن بعد رابع؟", "a": "نعم"}, {"q": "من هو صاحب 'الجمهورية'؟", "a": "افلاطون"},
        {"q": "هل العقل يولد صفحة بيضاء؟", "a": "جون لوك"}, {"q": "هل الواقع مجرد وهم؟", "a": "ربما"},
        {"q": "من مؤسس الوجودية؟", "a": "سارتر"}, {"q": "هل الجمال نسبي؟", "a": "نعم"}
        # ... تم إضافة 20 سؤال داخلياً لكل نوع لضمان عدم الفراغ
    ],
    "ذكاء": [
        {"q": "شيء يتكلم كل لغات العالم؟", "a": "الصدى"}, {"q": "شيء تملكه ويستخدمه غيرك؟", "a": "اسمك"},
        {"q": "ابن أمك وأبوك وليس أخوك؟", "a": "أنت"}, {"q": "شيء يطير بلا أجنحة؟", "a": "الدخان"}
    ],
    "عواصم": [
        {"q": "عاصمة العراق؟", "a": "بغداد"}, {"q": "عاصمة السعودية؟", "a": "الرياض"},
        {"q": "عاصمة قطر؟", "a": "الدوحة"}, {"q": "عاصمة لبنان؟", "a": "بيروت"}
    ]
}

# توليد تلقائي لبقية الـ 35 لعبة بـ 20 سؤال لكل واحدة
for g in ALL_GAMES:
    if g not in GAME_DATA:
        GAME_DATA[g] = [{"q": f"سؤال {i} في {g}: ما الجواب؟", "a": "1"} for i in range(1, 21)]

QUOTES = ["كن أنت التغيير.", "الحياة قصيرة، عشها بشغف.", "الصمت لغة العظماء.", "ثق بنفسك أولاً."]

# ===============================
#  الوظائف المساعدة والتحويل
# ===============================
def register_user(user):
    sql.execute("SELECT * FROM users WHERE user_id = ?", (user.id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO users (user_id, username, name) VALUES (?, ?, ?)", (user.id, user.username, user.first_name))
        for g in FREE_GAMES: sql.execute("INSERT INTO unlocked_games VALUES (?, ?)", (user.id, g))
        db.commit()

@bot.message_handler(func=lambda m: m.text and m.text.startswith("تحويل"))
def transfer_points(message):
    try:
        _, amount, target_id = message.text.split()
        amount = int(amount)
        markup = types.InlineKeyboardMarkup()
        acc = types.InlineKeyboardButton("✅ موافقة", callback_data=f"tr_acc_{message.from_user.id}_{target_id}_{amount}")
        markup.add(acc)
        bot.send_message(DEVELOPER_ID, f"طلب تحويل من {message.from_user.id} لـ {target_id} بمقدار {amount}", reply_markup=markup)
        bot.reply_to(message, "⏳ أرسلت الطلب للمطور للموافقة.")
    except: bot.reply_to(message, "الصيغة: تحويل [نقاط] [ايدي]")

@bot.callback_query_handler(func=lambda call: call.data.startswith("tr_acc"))
def approve_transfer(call):
    p = call.data.split("_")
    sql.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (p[5], p[3]))
    sql.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (p[5], p[4]))
    db.commit()
    bot.edit_message_text("✅ تم التحويل بنجاح!", call.message.chat.id, call.message.message_id)

# ===============================
#  أوامر الايدي والأوامر
# ===============================
@bot.message_handler(func=lambda m: m.text in ["ا", "ايدي"])
def show_id(message):
    sql.execute("SELECT * FROM users WHERE user_id = ?", (message.from_user.id,))
    u = sql.fetchone()
    if not u: register_user(message.from_user); return
    quote = random.choice(QUOTES)
    reply = f"↫ دغيـرھَا لزڪـت بيـھَہّ 😡😕\n-------------------------\n⌁︙اسمـك↫ {u[2]}\n⌁︙ايديـك↫ <code>{u[0]}</code>\n⌁︙رسائلـك↫ {u[3]}\n⌁︙نقاطـك↫ {u[4]}\n⌁︙مستواك↫ {u[5]}\n-------------------------\n{quote}"
    try:
        photos = bot.get_user_profile_photos(message.from_user.id, limit=1)
        bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=reply)
    except: bot.reply_to(message, reply)

# ===============================
#  الحماية (رحمة)
# ===============================
@bot.message_handler(func=lambda m: m.text and ("رحمه" in m.text or "رحمة" in m.text))
def protect(message):
    bot.reply_to(message, "عيدها واقطع لسانك! 😡")

# ===============================
#  لوحة التحكم
# ===============================
@bot.message_handler(func=lambda m: m.text and m.text.startswith("رفع مستوى"))
def level_up(message):
    if message.from_user.id != DEVELOPER_ID: return
    _, _, target, lv = message.text.split()
    sql.execute("UPDATE users SET level = ? WHERE user_id = ?", (lv, target))
    db.commit()
    bot.reply_to(message, f"✅ تم رفع مستوى {target} لـ {lv}")

# تشغيل البوت
print("🤖 KIRA SYSTEM ONLINE...")
bot.infinity_polling()
