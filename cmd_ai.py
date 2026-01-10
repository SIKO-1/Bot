# cmd_ai.py
import os
import telebot
import openai

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("❌ ضع OPENAI_API_KEY في البيئة")

openai.api_key = OPENAI_KEY

def handle(bot, message):
    chat_id = message.chat.id
    uid = message.from_user.id
    text = message.text

    # فقط نصوص
    if not text:
        return

    try:
        bot.send_chat_action(chat_id, "typing")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ومتطور بأسلوب الإمبراطور."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=500
        )

        answer = response.choices[0].message.content.strip()
        bot.send_message(chat_id, f"🤖 الإمبراطور يقول:\n{answer}")

    except Exception as e:
        bot.send_message(chat_id, f"❌ حدث خطأ أثناء الرد: {e}")
