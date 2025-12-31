import os, sqlite3, telebot, requests

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324 

# --- قاعدة بيانات الإمبراطورية ---
def get_db():
    conn = sqlite3.connect("kira_empire.db", check_same_thread=False)
    return conn

db_conn = get_db()
db_conn.execute("CREATE TABLE IF NOT EXISTS custom_cmds (cmd_name TEXT PRIMARY KEY, cmd_reply TEXT)")
db_conn.commit()

# --- محرك الذكاء الاصطناعي (Gemini Engine) ---
def ask_ai(text):
    try:
        # استخدام API يدعم العربية بذكاء حقيقي
        url = f"https://api.kenliejugar.com/free-ai/?text={text}"
        res = requests.get(url, timeout=5).json()
        output = res.get("response", "")
        return output if output else "أمرك مطاع يا إمبراطور، ماذا تريد؟"
    except:
        return "أسمعك يا إمبراطور، جاري معالجة طلبك."

# --- معالج الرسائل الذكي ---
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    uid = message.from_user.id
    text = message.text
    if not text: return

    # 1. ميزة "البرمجة بالشرح" (حصرياً للإمبراطور)
    # مثال: "اضف امر هلو - الرد يكون هلا والله"
    if uid == DEV_ID and ("اضف امر" in text or "أضف أمر" in text):
        if "-" in text:
            try:
                clean = text.replace("اضف امر", "").replace("أضف أمر", "").strip()
                cmd, reply = clean.split("-", 1)
                conn = get_db()
                conn.execute("INSERT OR REPLACE INTO custom_cmds VALUES (?, ?)", (cmd.strip(), reply.strip()))
                conn.commit()
                return bot.reply_to(message, f"✅ علم وينفذ! تم حفظ الأمر الجديد: <b>{cmd.strip()}</b>")
            except:
                return bot.reply_to(message, "⚠️ الصيغة: <code>اضف امر الاسم - الرد</code>")

    # 2. فحص الأوامر المخصصة التي تمت برمجتها
    conn = get_db()
    res = conn.execute("SELECT cmd_reply FROM custom_cmds WHERE cmd_name = ?", (text,)).fetchone()
    if res: return bot.send_message(message.chat.id, res[0])

    # 3. الدردشة بالذكاء الاصطناعي (رد فوري)
    ai_reply = ask_ai(text)
    bot.reply_to(message, ai_reply)

# --- التشغيل مع تنظيف الرسائل القديمة ---
if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True) # لتجاوز كل الرسائل القديمة المعلقة
