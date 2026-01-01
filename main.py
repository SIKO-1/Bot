import os, sqlite3, telebot, requests, random

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

# --- مخزن الردود الذكية (في حال تعطل الـ AI) ---
RANDOM_REPLIES = [
    "أنا معك يا إمبراطور، ماذا نحتاج أن نفعل اليوم؟",
    "نعم يا زعيم، هل تريد إضافة أمر جديد أم نلعب؟",
    "سمعتك جيداً، الإمبراطورية تحت سيطرتك!",
    "أنا جاهز لكل أوامرك، فقط اطلب واستمتع.",
    "ذكائي في خدمتك دائماً، هل نبدأ التحدي؟"
]

# --- محرك الذكاء الاصطناعي (API موثوق) ---
def ask_ai(text):
    try:
        # استخدام API بديل ومستقر جداً
        url = f"https://api.vkrprivate.repl.co/ai/chat?prompt={text}"
        res = requests.get(url, timeout=5).json()
        output = res.get("response", "")
        if output and len(output) > 2:
            return output
    except:
        pass
    return random.choice(RANDOM_REPLIES) # رد عشوائي ذكي بدلاً من تكرار جملة واحدة

# --- معالج الرسائل ---
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    uid = message.from_user.id
    text = message.text
    if not text: return

    # 1. أوامر الإمبراطور (أضف أمر)
    if uid == DEV_ID and ("اضف" in text or "أضف" in text) and "-" in text:
        try:
            clean = text.replace("اضف امر", "").replace("أضف أمر", "").strip()
            cmd, reply = clean.split("-", 1)
            conn = get_db()
            conn.execute("INSERT OR REPLACE INTO custom_cmds VALUES (?, ?)", (cmd.strip(), reply.strip()))
            conn.commit()
            return bot.reply_to(message, f"✅ تم الحفظ: <b>{cmd.strip()}</b>")
        except: pass

    # 2. فحص الأوامر المخصصة
    conn = get_db()
    res = conn.execute("SELECT cmd_reply FROM custom_cmds WHERE cmd_name = ?", (text,)).fetchone()
    if res: return bot.send_message(message.chat.id, res[0])

    # 3. الرد الفوري (AI أو رد إمبراطوري عشوائي)
    bot.reply_to(message, ask_ai(text))

# --- التشغيل الصاعق ---
if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True) # تجاوز كل الرسائل القديمة المسببة للتأخير
