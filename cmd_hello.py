# ملف: cmd_hello.py
import random
from aiogram import types
from bot_config import DEV_IDS  # قائمة المطورين والمالكين

# ======= الأوامر / الكلمات =======
HELLO_KEYWORDS = [
    "هلا", "امداك", "مح", "مُح", "ممحح", "مممحححح",
    "مححححح", "ها", "هاا", "هااااا", "نورت", "نورتي",
    "ءنجب", "انجب", "انجبي"
]

# ======= التعامل مع الرسائل =======
async def handle(message: types.Message, bot):
    if not message.text:
        return

    text = message.text.strip().lower()
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "صديقي"

    # ======= الردود =======
    if text in ["سلام عليكم", "السلام عليكم"]:
        await bot.send_message(message.chat.id, "وعليڪم السلام")
        return

    elif text in ["مح", "مُح", "ممحح", "مممحححح", "مححححح"]:
        await bot.send_message(message.chat.id, "مممحح شهلعسل 😫❤")
        return

    elif text in ["ها", "هاا", "هااااا"]:
        await bot.send_message(message.chat.id, "هاييمعود شسطرتنه")
        return

    elif text in ["نورت", "نورتي"]:
        await bot.send_message(message.chat.id, "نِٰـِۢﯛ̲رڪِٰـِۢ هـذَآ يآشُمعٍھَہّ")
        return

    elif text in ["ءنجب", "انجب", "انجبي"]:
        # لو المرسل مطور أو مالك
        if user_id in DEV_IDS:
            await bot.send_message(message.chat.id, "مطور مگدر ارد عليك")
        else:
            await bot.send_message(message.chat.id, "انجب انتَ لتنسحل")
        return

    elif text == "هلا":
        await bot.send_message(message.chat.id, f"هلوات 🫦 يا {user_name}")
        return

    elif text == "امداك":
        await bot.send_message(message.chat.id, f"امداك انتَ")
        return

    # ======= الردود العشوائية =======
    fun_replies = [
        f"شلونك يا {user_name}؟ 😎",
        "هاه شكو ماكو؟ 🤔",
        "عيونك حلوة اليوم 👀",
        "والله الجو حلو هسه 🌤",
        "هاي، تحية إمبراطورية لك 👑",
        "ههههه شكو هاي؟ 😂"
    ]
    reply = random.choice(fun_replies)
    await bot.send_message(message.chat.id, reply)


# ======= الترحيب بالعضو الجديد =======
async def handle_new_member(message: types.Message, bot):
    if not message.new_chat_members:
        return

    for new_member in message.new_chat_members:
        name = new_member.first_name or "عضو جديد"
        welcome_msg = f"✨ نورتنا يا [{name}](tg://user?id={new_member.id})! 👑"
        await bot.send_message(message.chat.id, welcome_msg, parse_mode="Markdown")
