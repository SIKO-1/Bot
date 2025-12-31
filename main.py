import os, sqlite3, telebot, requests, random
from telebot import types

# --- الإعدادات الأساسية ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324  # ايدي الإمبراطور الخاص بك

# --- قاعدة البيانات ---
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 1000, role TEXT DEFAULT 'عضو')")
sql.execute("CREATE TABLE IF NOT EXISTS custom_cmds (cmd_name TEXT PRIMARY KEY, cmd_reply TEXT)")
sql.execute("CREATE TABLE IF NOT EXISTS memory (user_id INTEGER PRIMARY KEY, chat_log TEXT)")
db.commit()

# --- محرك الذكاء الاصطناعي المطور ---
def ask_ai(text, user_id):
    try:
        # جلب الذاكرة السابقة
        sql.execute("SELECT chat_log FROM memory WHERE user_id = ?", (user_id,))
        past = sql.fetchone()
        context = past[0] if past else ""

        # استخدام API جديد ومستقر (Gemini Engine)
        url = f"https://api.kenliejugar.com/free-ai/?text={context} {text}"
        response = requests.get(url).json()
        res = response.get("response", "")

        if not res: # خطة بديلة إذا كان الرد فارغاً
             return "أمرك مطاع يا إمبراطور، ماذا تريدني أن أفعل الآن؟"

        # تحديث الذاكرة
        new_memory = (context + f" user: {text} bot: {res}")[-500:] 
        sql.execute("INSERT OR REPLACE INTO memory VALUES (?, ?)", (user_id, new_memory))
        db.commit()
        return res
    except:
        return "أنا أسمعك يا إمبراطور، لكن يبدو أن هناك ضغطاً على خوادم الذكاء الاصطناعي. كيف يمكنني مساعدتك يدوياً؟"

# --- معالج الرسائل الذكي ---
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    uid = message.from_user.id
    text = message.text
    if not text: return

    # 1. نظام "البرمجة بالشرح" للإمبراطور
    if uid == DEV_ID and ("أضف أمر" in text or "اضف امر" in text):
        # نطلب من الذكاء الاصطناعي استخراج الأمر والرد من شرحك
        raw_data = ask_ai(f"استخرج من النص التالي 'الأمر' و 'الرد المناسب' وضعهما بصيغة (الاسم|الرد) فقط دون كلام إضافي: {text}", uid)
        if "|" in raw_data:
            name, reply = raw_data.split("|", 1)
            sql.execute("INSERT OR REPLACE INTO custom_cmds VALUES (?, ?)", (name.strip(), reply.strip()))
            db.commit()
            return bot.reply_to(message, f"✅ علم وينفذ! تم إضافة أمر <b>{name.strip()}</b> بناءً على شرحك.")

    # 2. فحص الأوامر المخصصة المحفوظة
    sql.execute("SELECT cmd_reply FROM custom_cmds WHERE cmd_name = ?", (text,))
    res = sql.fetchone()
    if res: return bot.send_message(message.chat.id, res[0])

    # 3. الألعاب (مدمجة للاستقرار)
    if text == "العاب":
        return bot.reply_to(message, "🕹️ <b>الألعاب المتاحة:</b>\n🔓 عواصم\n🔓 دين\n🔓 ذكاء\n(اكتب اسم اللعبة للبدء)")

    # 4. الرد بالذكاء الاصطناعي المتطور
    bot.send_chat_action(message.chat.id, 'typing')
    ai_reply = ask_ai(text, uid)
    bot.reply_to(message, ai_reply)

bot.infinity_polling(skip_pending=True)
