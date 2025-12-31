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

# --- محرك الذكاء الاصطناعي المتطور (API جديد) ---
def ask_ai(text):
    try:
        # محرك ذكاء اصطناعي جديد يدعم العربية بطلاقة
        url = f"https://api.aggelos-007.xyz/ai?prompt={text}"
        res = requests.get(url, timeout=7).json()
        output = res.get("response", "")
        if output:
            return output
        else:
            return "عذراً يا إمبراطور، لم أستطع صياغة رد ذكي حالياً."
    except:
        return "⚠️ يبدو أن هناك ضغطاً على خوادم الذكاء الاصطناعي."

# --- معالج الرسائل ---
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    uid = message.from_user.id
    text = message.text
    if not text: return

    # 1. أوامر الإمبراطور (أضف أمر بالشرح)
    if uid == DEV_ID and ("اضف امر" in text or "أضف أمر" in text):
        if "-" in text:
            try:
                clean = text.replace("اضف امر", "").replace("أضف أمر", "").strip()
                cmd, reply = clean.split("-", 1)
                conn = get_db()
                conn.execute("INSERT OR REPLACE INTO custom_cmds VALUES (?, ?)", (cmd.strip(), reply.strip()))
                conn.commit()
                return bot.reply_to(message, f"✅ تم الحفظ يا إمبراطور: <b>{cmd.strip()}</b>")
            except:
                return bot.reply_to(message, "⚠️ استخدم: اضف امر الاسم - الرد")

    # 2. فحص الأوامر المخصصة
    conn = get_db()
    res = conn.execute("SELECT cmd_reply FROM custom_cmds WHERE cmd_name = ?", (text,)).fetchone()
    if res: return bot.send_message(message.chat.id, res[0])

    # 3. الرد بالذكاء الاصطناعي (رد مباشر وسريع)
    ai_reply = ask_ai(text)
    bot.reply_to(message, ai_reply)

# --- التشغيل ---
if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
