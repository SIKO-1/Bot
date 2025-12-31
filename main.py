import os, sqlite3, telebot, requests
from telebot import types

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324  # ايديك الخاص يا إمبراطور

# --- دالة الاتصال الآمن بقاعدة البيانات ---
def get_db():
    # استخدام check_same_thread=False لحل خطأ البرمجة في السجلات
    conn = sqlite3.connect("kira_empire.db", check_same_thread=False)
    return conn, conn.cursor()

# إنشاء الجداول لأول مرة
db_conn, sql = get_db()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 1000, role TEXT DEFAULT 'عضو')")
sql.execute("CREATE TABLE IF NOT EXISTS custom_cmds (cmd_name TEXT PRIMARY KEY, cmd_reply TEXT)")
sql.execute("CREATE TABLE IF NOT EXISTS memory (user_id INTEGER PRIMARY KEY, chat_log TEXT)")
db_conn.commit()

# --- محرك الذكاء الاصطناعي المستقر ---
def ask_ai(text, user_id):
    try:
        conn, cursor = get_db()
        cursor.execute("SELECT chat_log FROM memory WHERE user_id = ?", (user_id,))
        past = cursor.fetchone()
        context = past[0] if past else ""

        # استخدام API جديد يدعم العربية والذاكرة
        url = f"https://api.popcat.xyz/chatbot?msg={text}&owner=Kira&botname=KeraBot"
        res = requests.get(url).json().get("response", "أنا معك يا إمبراطور، كيف أخدمك؟")

        # حفظ الذاكرة
        new_memory = (context + f" user: {text} bot: {res}")[-500:]
        cursor.execute("INSERT OR REPLACE INTO memory VALUES (?, ?)", (user_id, new_memory))
        conn.commit()
        conn.close()
        return res
    except:
        return "أمرك مطاع يا إمبراطور، ماذا يدور في ذهنك؟"

# --- معالج الرسائل ---
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    uid = message.from_user.id
    text = message.text
    if not text: return

    conn, cursor = get_db()

    # 1. ميزة الإضافة بالشرح (لك فقط)
    if uid == DEV_ID and ("أضف أمر" in text or "اضف امر" in text):
        ai_info = ask_ai(f"استخرج اسم الأمر والرد منه فقط بصيغة (الاسم|الرد): {text}", uid)
        if "|" in ai_info:
            name, reply = ai_info.split("|", 1)
            cursor.execute("INSERT OR REPLACE INTO custom_cmds VALUES (?, ?)", (name.strip(), reply.strip()))
            conn.commit()
            conn.close()
            return bot.reply_to(message, f"✅ أبشر! تم إضافة أمر: <b>{name.strip()}</b>")

    # 2. فحص الأوامر المخصصة
    cursor.execute("SELECT cmd_reply FROM custom_cmds WHERE cmd_name = ?", (text,))
    res = cursor.fetchone()
    conn.close()
    if res: return bot.send_message(message.chat.id, res[0])

    # 3. الرد بالذكاء الاصطناعي
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, ask_ai(text, uid))

bot.infinity_polling(skip_pending=True)
