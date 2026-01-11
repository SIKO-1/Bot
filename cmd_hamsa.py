import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# تخزين مؤقت للهمسات
whispers = {}  # key: chat_id_message_id, value: {"from": user_id, "to": user_id, "text": str}

def handle(bot: telebot.TeleBot, message):
    uid = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip()

    # أمر "همسه" فقط في المجموعات
    if text == "همسه" and message.chat.type != "private":
        reply = bot.reply_to(message, f"⌔︙تم تحديد الهمسه الى » @{message.reply_to_message.from_user.username if message.reply_to_message else 'الشخص'}\n\n⌔︙اضغط على الزر لكتابه الهمسه")
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✉️ إرسال الهمسه", callback_data=f"send_whisper:{reply.message_id}"))
        bot.edit_message_reply_markup(chat_id, reply.message_id, reply_markup=markup)

# ======================
# التعامل مع أزرار الهمسه
# ======================
def callback_handler(bot: telebot.TeleBot, call: CallbackQuery):
    data = call.data

    if data.startswith("send_whisper:"):
        original_msg_id = int(data.split(":")[1])
        chat_id = call.message.chat.id
        uid = call.from_user.id

        # نرسل رسالة خاصة للشخص اللي ضغط الزر ليكتب الهمسة
        bot.answer_callback_query(call.id)
        bot.send_message(uid, "⌔︙حسناً, ارسل الهمسة الان")

        # تسجيل أنه هذا الشخص مرتبط بالهمسة
        whispers[uid] = {"chat_id": chat_id, "original_msg_id": original_msg_id, "from": uid}

# ======================
# استقبال الرسائل الخاصة للهمسه
# ======================
def handle_private(bot: telebot.TeleBot, message):
    uid = message.from_user.id
    if uid not in whispers:
        return

    whisper_info = whispers.pop(uid)
    chat_id = whisper_info["chat_id"]
    original_msg_id = whisper_info["original_msg_id"]
    from_user = whisper_info["from"]

    to_user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    from_user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

    # إرسال الهمسة في المجموعة
    bot.send_message(chat_id,
        f"🔒 هذه همسة سرية لك ↫ {to_user_mention}\n"
        f"الهمسة من ↫ {from_user_mention}\n\n"
        f"{message.text}")

# ======================
# تسجيل Callback
# ======================
def register_callbacks(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("send_whisper:"))
    def callback(call):
        callback_handler(bot, call)
