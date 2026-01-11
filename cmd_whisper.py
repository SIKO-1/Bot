# cmd_whisper.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import uuid

# تخزين الهمسات مؤقتاً بالذاكرة
WHISPERS = {}

def handle(bot, message, *args):
    if not message.text:
        return

    text = message.text.strip()

    # الصيغة: همسة @user النص
    if not text.startswith("همسة"):
        return

    if message.chat.type == "private":
        bot.reply_to(message, "❌ الهمسة تعمل داخل المجموعات فقط.")
        return

    parts = text.split(maxsplit=2)
    target_user = None
    whisper_text = None

    # حالة الرد على شخص
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        whisper_text = text.replace("همسة", "", 1).strip()

    # حالة المنشن
    elif len(parts) >= 3 and parts[1].startswith("@"):
        username = parts[1][1:]
        whisper_text = parts[2]

        # نحاول نلقط المستخدم من الكروب
        for member in bot.get_chat_administrators(message.chat.id):
            if member.user.username == username:
                target_user = member.user
                break

        if not target_user:
            bot.reply_to(message, "❌ ما كدرت أحدد المستخدم. جرب الرد عليه.")
            return
    else:
        bot.reply_to(message, "❌ الصيغة:\nهمسة (بالرد) النص\nأو\nهمسة @user النص")
        return

    if not whisper_text:
        bot.reply_to(message, "❌ اكتب نص الهمسة.")
        return

    whisper_id = str(uuid.uuid4())

    WHISPERS[whisper_id] = {
        "to": target_user.id,
        "text": whisper_text
    }

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="👁️ قراءة الهمسة",
            callback_data=f"whisper:{whisper_id}"
        )
    )

    bot.send_message(
        message.chat.id,
        f"🔒 همسة سرّية موجهة إلى @{target_user.username or target_user.first_name}",
        reply_markup=kb
    )


def handle_callback(bot, call):
    if not call.data.startswith("whisper:"):
        return

    whisper_id = call.data.split(":", 1)[1]
    data = WHISPERS.get(whisper_id)

    if not data:
        bot.answer_callback_query(call.id, "❌ هذه الهمسة انتهت.")
        return

    if call.from_user.id != data["to"]:
        bot.answer_callback_query(call.id, "🚫 هذه الهمسة مو إلك.")
        return

    bot.answer_callback_query(call.id, "📩 هذه همستك")
    bot.send_message(call.from_user.id, f"💬 همسة:\n\n{data['text']}")

    # حذف الهمسة بعد القراءة
    del WHISPERS[whisper_id]
