import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import db_manager  # إذا عندك أي حاجة لتخزين مؤقت ممكن تضيف هنا

# ======================
# موديل همسة
# ======================
def handle(bot: telebot.TeleBot, message: Message):
    if message.text and message.text.lower() == "همسه" and message.reply_to_message:
        target_user = message.reply_to_message.from_user
        sender_user = message.from_user

        # إنشاء زر للخاص
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📩 إرسال الهمسة", callback_data=f"send_whisper:{sender_user.id}:{target_user.id}"))

        bot.reply_to(message,
                     f"⌔︙تم تحديد الهمسه إلى » {target_user.mention}\n"
                     f"⌔︙اضغط على الزر لكتابة الهمسه",
                     reply_markup=markup)

# ======================
# التعامل مع الزر
# ======================
def handle_callback(bot: telebot.TeleBot, call):
    data = call.data
    if data.startswith("send_whisper"):
        _, sender_id, target_id = data.split(":")
        sender_id = int(sender_id)
        target_id = int(target_id)

        # تحقق: فقط المرسل يقدر يرسل الهمسة
        if call.from_user.id != sender_id:
            bot.answer_callback_query(call.id, "❌ هذا الزر ليس لك!", show_alert=True)
            return

        bot.answer_callback_query(call.id)
        bot.send_message(sender_id, "⌔︙حسناً، أرسل الهمسة الآن")

        # تسجيل الحالة في dictionary مؤقتة
        if not hasattr(bot, "waiting_whispers"):
            bot.waiting_whispers = {}
        bot.waiting_whispers[sender_id] = target_id

# ======================
# استقبال الرسالة في الخاص
# ======================
def handle_private(bot: telebot.TeleBot, message: Message):
    if not hasattr(bot, "waiting_whispers"):
        return
    sender_id = message.from_user.id
    if sender_id not in bot.waiting_whispers:
        return

    target_id = bot.waiting_whispers.pop(sender_id)
    # إرسال الهمسة للمجموعة كرسالة سرية للشخص
    # نفترض نرسلها في نفس الشات الأصلي، هنا ممكن تخزن chat_id أصلي إذا احتجت
    try:
        bot.send_message(target_id,
                         f"هذه همسة سرية لك ↫ {message.from_user.mention}\n"
                         f"الهمسة من ↫ {message.from_user.mention}\n\n"
                         f"💌 {message.text}")
    except:
        bot.send_message(sender_id, "❌ لم أستطع إرسال الهمسة للمستلم.")

    # رسالة للمجموعة: زر عرض الهمسة
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("💌 عرض الهمسة", callback_data=f"view_whisper:{sender_id}:{target_id}:{message.text}"))
    # افترض أن message.forward_from_chat هو الشات الأصلي، أو احفظ chat_id
    # لو ماعندك chat_id أصلي خليه الشخص يعيد توجيه الرسالة للمجموعة
    # هنا مجرد مثال
    # bot.send_message(chat_id_original, f"🔒 همسة جديدة!", reply_markup=markup)

# ======================
# عرض الهمسة لأي شخص يضغط الزر
# ======================
def handle_view(bot: telebot.TeleBot, call):
    data = call.data
    if data.startswith("view_whisper"):
        _, sender_id, target_id, text = data.split(":", 3)
        sender_id = int(sender_id)
        target_id = int(target_id)

        if call.from_user.id == target_id:
            bot.answer_callback_query(call.id, "📬 هذه همستك! استمتع بها 😉", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "😏 ههه، هذه ليست همستك، لا تحاول التلاعب 😉", show_alert=True)
