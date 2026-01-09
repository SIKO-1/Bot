import random
from telebot import TeleBot
from telebot.types import Message

# ======================
# إعدادات
# ======================

MARRIAGE_IMAGE = "https://up6.cc/2026/10/176800027196491.jpg"
# ↑ غير الرابط فقط

marriages = {}  # chat_id: {user_id: partner_id}

# ======================
# أمر زوجني
# ======================

def register_marriage_commands(bot: TeleBot):

    @bot.message_handler(commands=["زوجني"])
    def marry_random(message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        if user_id in marriages.get(chat_id, {}):
            bot.reply_to(message, "😅 انت متزوج أصلًا، تريد تفضحنا؟")
            return

        members = bot.get_chat_administrators(chat_id)
        users = [m.user for m in members if not m.user.is_bot and m.user.id != user_id]

        if not users:
            bot.reply_to(message, "😐 ماكو ناس أتزوجهم هسه")
            return

        partner = random.choice(users)

        marriages.setdefault(chat_id, {})[user_id] = partner.id
        marriages.setdefault(chat_id, {})[partner.id] = user_id

        caption = f"""
💍 تم الزواج بنجاح!

🤵‍♂️ الزوج: @{message.from_user.username or message.from_user.first_name}
👰‍♀️ الزوجة: @{partner.username or partner.first_name}

مبروك 🎉😂
        """

        bot.send_photo(chat_id, MARRIAGE_IMAGE, caption=caption)

    # ======================
    # أمر طلقني
    # ======================

    @bot.message_handler(commands=["طلقني"])
    def divorce(message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        if user_id not in marriages.get(chat_id, {}):
            bot.reply_to(message, "😐 انت مو متزوج أصلاً")
            return

        partner_id = marriages[chat_id].pop(user_id)
        marriages[chat_id].pop(partner_id, None)

        bot.reply_to(message, "💔 تم الطلاق… الله يعوض 😂")
