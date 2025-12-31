import os, sqlite3, telebot, requests, random
from telebot import types

# --- الإعدادات الأساسية ---
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324  # ايدي الإمبراطور

# --- قاعدة البيانات المتطورة ---
db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 1000, role TEXT DEFAULT 'عضو')")
sql.execute("CREATE TABLE IF NOT EXISTS custom_cmds (cmd_name TEXT PRIMARY KEY, cmd_reply TEXT)")
sql.execute("CREATE TABLE IF NOT EXISTS memory (user_id INTEGER PRIMARY KEY, chat_log TEXT)")
db.commit()

# --- بنك الألعاب والأسئلة (مدمج لمنع الخطأ) ---
GAMES_DATA = {
    "عواصم": {"buy": 200, "win": 50, "q": "عاصمة العراق؟", "a": "بغداد"},
    "دين": {"buy": 200, "win": 50, "q": "أطول سورة؟", "a": "البقرة"},
    "ذكاء": {"buy": 200, "win": 50, "q": "حاصل 5+5؟", "a": "10"}
}
RANDOM_FREE_GAMES = list(GAMES_DATA.keys())[:2] # أول لعبتين مجانية دائماً لضمان الاستقرار

# --- محرك الذكاء الاصطناعي (جيمناي) مع الذاكرة ---
def ask_ai(text, user_id):
    try:
        sql.execute("SELECT chat_log FROM memory WHERE user_id = ?", (user_id,))
        past = sql.fetchone()
        context = past[0] if past else ""
        
        # ربط الـ API بالذكاء الاصطناعي
        url = f"https://darkness.ashlynn.workers.dev/chat?prompt={context} {text}"
        res = requests.get(url).json().get("response", "أمرك مطاع يا إمبراطور.")
        
        # تحديث الذاكرة
        new_memory = (context + f" user: {text} bot: {res}")[-500:] 
        sql.execute("INSERT OR REPLACE INTO memory VALUES (?, ?)", (user_id, new_memory))
        db.commit()
        return res
    except: return "عقلي مشوش قليلاً، أعد المحاولة."

# --- المعالج الرئيسي لجميع الرسائل ---
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    uid = message.from_user.id
    text = message.text
    if not text: return

    # 1. إضافة أمر بالشرح (للإمبراطور فقط)
    if uid == DEV_ID and ("أضف أمر" in text or "اضف امر" in text):
        raw_data = ask_ai(f"حول هذا الشرح لرد بصيغة (الاسم|الرد): {text}", uid)
        if "|" in raw_data:
            name, reply = raw_data.split("|")
            sql.execute("INSERT OR REPLACE INTO custom_cmds VALUES (?, ?)", (name.strip(), reply.strip()))
            db.commit()
            return bot.reply_to(message, f"✅ تم استيعاب شرحك! إضافة أمر: <b>{name}</b>")

    # 2. فحص الأوامر المخصصة
    sql.execute("SELECT cmd_reply FROM custom_cmds WHERE cmd_name = ?", (text,))
    res = sql.fetchone()
    if res: return bot.send_message(message.chat.id, res[0])

    # 3. نظام الألعاب
    if text == "العاب":
        txt = "🎭 <b>إمبراطورية الألعاب</b>\n\n"
        for g in GAMES_DATA: txt += f"🔓 {g}\n"
        return bot.reply_to(message, txt)
    
    if text in GAMES_DATA:
        q = GAMES_DATA[text]
        return bot.reply_to(message, f"🕹️ <b>{text}:</b>\n\n❓ {q['q']}\n(أجب بالرد)")

    # 4. الرد بالذكاء الاصطناعي (إذا لم يكن مما سبق)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, ask_ai(text, uid))

bot.infinity_polling(skip_pending=True)
