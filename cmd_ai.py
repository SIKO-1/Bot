import telebot
from telebot.types import Message
import db_manager
import openai  # تحتاج مفتاح OpenAI API في متغير البيئة OPENAI_API_KEY
import os
import traceback

# ======================
# إعداد OpenAI
# ======================
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    print("❌ OpenAI API key غير موجودة")
openai.api_key = OPENAI_KEY

# ======================
# المساعد الذكي
# ======================
def handle(bot: telebot.TeleBot, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip() if message.text else None

    # فقط الرسائل النصية
    if not text:
        return

    # تحقق من تفعيل AI في المجموعة (افتراضياً مفعل)
    ai_enabled = db_manager.get_ai_enabled(chat_id)
    if not ai_enabled:
        return

    # رد على المستخدم بأسلوب إمبراطوري وفلسفي
    try:
        prompt = f"أنت إمبراطور حكيم وفلسفي. أجب على المستخدم بطريقة عميقة وملهمة:\n\n{message.from_user.first_name}: {text}\nإجابتك:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=250,
            temperature=0.8,
        )
        answer = response.choices[0].text.strip()
        if answer:
            bot.reply_to(message, f"👑 الإمبراطور: {answer}")
    except Exception as e:
        traceback.print_exc()
        bot.reply_to(message, f"⚠️ حدث خطأ أثناء الرد: {str(e)}")
