import os, sqlite3, telebot, requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DEV_ID = 5860391324 

# --- دالة الذكاء الاصطناعي لتحويل كلامك لكود ---
def translate_to_code(user_request):
    try:
        prompt = f"تحويل الطلب التالي إلى كود بايثون لمكتبة pyTelegramBotAPI: {user_request}. أريد الكود فقط."
        url = f"https://api.kenliejugar.com/free-ai/?text={prompt}"
        res = requests.get(url, timeout=10).json()
        return res.get("response", "")
    except: return None

@bot.message_handler(func=lambda m: m.from_user.id == DEV_ID)
def auto_developer(message):
    text = message.text
    
    # 1. ميزة البرمجة بالشرح
    if text.startswith("حدث برمجتك"):
        request = text.replace("حدث برمجتك", "").strip()
        bot.reply_to(message, "🚀 جاري تحليل طلبك وبرمجة الميزة...")
        
        new_code = translate_to_code(request)
        if new_code:
            try:
                # تحذير: هذا الجزء ينفذ كود مباشرة (حصري للإمبراطور)
                exec(new_code, globals()) 
                bot.reply_to(message, "✅ تم تحديث إعداداتي بنجاح! جرب الميزة الآن.")
            except Exception as e:
                bot.reply_to(message, f"❌ فشلت البرمجة التلقائية.\nالخطأ: {e}")
        else:
            bot.reply_to(message, "عذراً يا إمبراطور، لم أستطع فهم الشرح البرمجي.")

    # 2. إضافة الأزرار والأوامر العادية
    elif "اضف ازرار" in text:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("قناة الإمبراطورية", url="https://t.me/your_channel")
        markup.add(btn1)
        bot.send_message(message.chat.id, "تم إضافة الأزرار بنجاح!", reply_markup=markup)

# تشغيل البوت مع تنظيف الرسائل
bot.infinity_polling(skip_pending=True)
