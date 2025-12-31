import os, sqlite3, telebot, requests

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324 

# --- قاعدة البيانات ---
def get_db():
    conn = sqlite3.connect("kira_empire.db", check_same_thread=False)
    return conn

db_conn = get_db()
db_conn.execute("CREATE TABLE IF NOT EXISTS custom_cmds (cmd_name TEXT PRIMARY KEY, cmd_reply TEXT)")
db_conn.commit()

# --- محرك الذكاء الاصطناعي (رد مباشر) ---
def ask_ai(text):
    try:
        # تقليل وقت المهلة (Timeout) لضمان عدم التأخير
        url = f"https://api.simsimi.vn/v1/simtalk"
        res = requests.post(url, data={'text': text, 'lc': 'ar'}, timeout=3).json()
        return res.get("message", "أمرك مطاع.")
    except:
        return "أسمعك يا إمبراطور، ماذا تريد؟"

# --- معالج الرسائل ---
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    uid = message.from_user.id
    text = message.text
    if not text: return

    # 1. أوامر الإضافة السريعة (اسم - رد)
    if uid == DEV_ID and "-" in text and ("اضف" in text or "أضف" in text):
        try:
            clean_text = text.replace("اضف امر", "").replace("أضف أمر", "").strip()
            name, reply = clean_text.split("-", 1)
            conn = get_db()
            conn.execute("INSERT OR REPLACE INTO custom_cmds VALUES (?, ?)", (name.strip(), reply.strip()))
            conn.commit()
            return bot.reply_to(message, f"✅ تم حفظ الأمر: {name.strip()}")
        except: pass

    # 2. فحص الأوامر المخصصة
    conn = get_db()
    res = conn.execute("SELECT cmd_reply FROM custom_cmds WHERE cmd_name = ?", (text,)).fetchone()
    if res: return bot.send_message(message.chat.id, res[0])

    # 3. الرد الفوري بالذكاء الاصطناعي (تم حذف Typing Action)
    bot.reply_to(message, ask_ai(text))

# --- التشغيل النهائي ---
if __name__ == "__main__":
    bot.remove_webhook()
    # تجاهل الرسائل القديمة للبدء فوراً
    bot.infinity_polling(skip_pending=True)
