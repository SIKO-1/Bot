import os, sqlite3, telebot, requests
from telebot import types
import games_system as gs

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324  # ايدي الإمبراطور

db = sqlite3.connect("kira_empire.db", check_same_thread=False)
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 1000, role TEXT)")
sql.execute("CREATE TABLE IF NOT EXISTS custom_cmds (cmd_name TEXT PRIMARY KEY, cmd_reply TEXT)")
# جدول الذاكرة
sql.execute("CREATE TABLE IF NOT EXISTS memory (user_id INTEGER, chat_log TEXT)")
db.commit()

def ask_ai(text, user_id):
    try:
        # جلب الذاكرة السابقة
        sql.execute("SELECT chat_log FROM memory WHERE user_id = ?", (user_id,))
        past = sql.fetchone()
        context = past[0] if past else ""
        
        url = f"https://darkness.ashlynn.workers.dev/chat?prompt={context} {text}"
        res = requests.get(url).json().get("response", "عذراً يا إمبراطور.")
        
        # تحديث الذاكرة (حفظ آخر جزء من الحوار)
        new_memory = (context + f" user: {text} bot: {res}")[-500:] 
        sql.execute("INSERT OR REPLACE INTO memory VALUES (?, ?)", (user_id, new_memory))
        db.commit()
        return res
    except: return "⚠️ عطل فني في الذاكرة."

@bot.message_handler(func=lambda m: True)
def main_handler(message):
    uid = message.from_user.id
    text = message.text

    # 1. ميزة إضافة الأمر بالشرح (للمطور فقط)
    if uid == DEV_ID and ("أضف أمر" in text or "اضف امر" in text):
        ai_logic = ask_ai(f"استخرج اسم الأمر والرد المناسب من هذا الشرح بصيغة (الاسم|الرد): {text}", uid)
        if "|" in ai_logic:
            name, reply = ai_logic.split("|")
            sql.execute("INSERT OR REPLACE INTO custom_cmds VALUES (?, ?)", (name.strip(), reply.strip()))
            db.commit()
            return bot.reply_to(message, f"✅ فهمتك يا إمبراطور! تم إضافة أمر: <b>{name}</b>")

    # 2. فحص الأوامر المخصصة
    sql.execute("SELECT cmd_reply FROM custom_cmds WHERE cmd_name = ?", (text,))
    res = sql.fetchone()
    if res: return bot.send_message(message.chat.id, res[0])

    # 3. الألعاب
    if text == "العاب":
        return bot.reply_to(message, gs.get_games_menu([]))
    elif text in gs.GAMES_DATA.keys():
        return gs.start_game_logic(bot, message, text)

    # 4. الرد بالذكاء الاصطناعي مع الذاكرة
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, ask_ai(text, uid))

bot.infinity_polling()
