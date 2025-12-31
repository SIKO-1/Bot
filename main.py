import os, sqlite3, telebot, requests, time

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324 

# --- معالجة قاعدة البيانات بأمان ---
def get_db():
    # استخدام الاتصال المحلي لتجنب أخطاء الـ Threads
    conn = sqlite3.connect("kira_empire.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL") # تسريع العمليات
    return conn

# إنشاء الجداول
db = get_db()
db.execute("CREATE TABLE IF NOT EXISTS custom_cmds (cmd_name TEXT PRIMARY KEY, cmd_reply TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS memory (user_id INTEGER PRIMARY KEY, chat_log TEXT)")
db.commit()

# --- محرك الذكاء الاصطناعي البديل والأكثر استقراراً ---
def ask_ai(text, user_id):
    try:
        # نظام الرد السريع لضمان عدم التعليق
        url = f"https://api.simsimi.vn/v1/simtalk"
        payload = {'text': text, 'lc': 'ar'}
        res = requests.post(url, data=payload).json().get("message", "أنا أسمعك يا إمبراطور.")
        return res
    except:
        return "أمرك مطاع، كيف يمكنني مساعدتك؟"

# --- معالج الرسائل ---
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    uid = message.from_user.id
    text = message.text
    if not text: return

    # 1. أوامر الإمبراطور (أضف أمر بالشرح)
    if uid == DEV_ID and ("أضف أمر" in text or "اضف امر" in text):
        # ذكاء اصطناعي بسيط للاستخراج اليدوي لتجنب تعليق الـ API
        if "-" in text:
            parts = text.replace("اضف امر", "").strip().split("-")
            name, reply = parts[0].strip(), parts[1].strip()
            db.execute("INSERT OR REPLACE INTO custom_cmds VALUES (?, ?)", (name, reply))
            db.commit()
            return bot.reply_to(message, f"✅ تم إضافة الأمر: <b>{name}</b>")

    # 2. فحص الأوامر المخصصة
    res = db.execute("SELECT cmd_reply FROM custom_cmds WHERE cmd_name = ?", (text,)).fetchone()
    if res: return bot.send_message(message.chat.id, res[0])

    # 3. الرد التلقائي/الذكاء الاصطناعي
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, ask_ai(text, uid))

# --- تشغيل البوت مع حل مشكلة Conflict 409 ---
if __name__ == "__main__":
    print("🚀 جاري تشغيل الإمبراطورية...")
    bot.remove_webhook() # حذف أي ارتباط قديم
    time.sleep(1) # انتظار ثانية للتأكد من إغلاق الجلسات السابقة
    bot.infinity_polling(skip_pending=True) # تجاهل الرسائل القديمة المعلقة
