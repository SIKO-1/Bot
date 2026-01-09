# cmd_marriage.py
import random
from telebot.types import Message
import db_marriage
from telebot import types

MARRIAGE_IMAGE = "https://up6.cc/2026/10/176800027196491.jpg"

def love_text(percent):
    if percent >= 95:
        return "💖 حبكما نار 🔥 ملك/ة جمال الحب!"
    if percent >= 80:
        return "😍 اثنين محبوبين بكل معنى الكلمة!"
    if percent >= 65:
        return "😘 نصيبكم حلو، استمتعوا سوا!"
    if percent >= 50:
        return "💘 نصيبكم متوسط، حاولوا تزيدوا الحب!"
    return "😅 الحب ضعيف، بس يمكن يتحسن!"

def register_marriage(bot):

    # ======================
    # زوجني عشوائي
    # ======================
    @bot.message_handler(func=lambda m: m.text == "زوجني")
    def marry_random(message: Message):
        chat_id = message.chat.id
        user = message.from_user

        if db_marriage.is_married(chat_id, user.id):
            bot.reply_to(message, "😅 انت متزوج أصلاً")
            return

        members = bot.get_chat_administrators(chat_id)
        users = [m.user for m in members if not m.user.is_bot and m.user.id != user.id and not db_marriage.is_married(chat_id, m.user.id)]

        if not users:
            bot.reply_to(message, "😐 ماكو أحد أعزابي")
            return

        partner = random.choice(users)
        db_marriage.marry(chat_id, user.id, partner.id)
        percent = db_marriage.marriages[chat_id][user.id]["love_percent"]
        dowry = db_marriage.marriages[chat_id][user.id]["dowry"]

        bot.send_photo(chat_id, MARRIAGE_IMAGE, caption=f"""
💍 زواج عشوائي

🤵 {user.first_name}
👰 {partner.first_name}

💸 المهر: {dowry} ذهب
{love_text(percent)}
""")

    # ======================
    # زوجني بالرد
    # ======================
    @bot.message_handler(func=lambda m: m.text == "زوجني" and m.reply_to_message)
    def marry_reply(message: Message):
        chat_id = message.chat.id
        user = message.from_user
        partner = message.reply_to_message.from_user

        if partner.is_bot:
            bot.reply_to(message, "🤖 البوتات ما تتزوج")
            return

        if db_marriage.is_married(chat_id, user.id) or db_marriage.is_married(chat_id, partner.id):
            bot.reply_to(message, "😅 أحدكم متزوج")
            return

        db_marriage.marry(chat_id, user.id, partner.id)
        percent = db_marriage.marriages[chat_id][user.id]["love_percent"]
        dowry = db_marriage.marriages[chat_id][user.id]["dowry"]

        bot.send_photo(chat_id, MARRIAGE_IMAGE, caption=f"""
💍 زواج بالرد

🤵 {user.first_name}
👰 {partner.first_name}

💸 المهر: {dowry} ذهب
{love_text(percent)}
""")

    # ======================
    # زوجني بالإيدي
    # ======================
    @bot.message_handler(func=lambda m: m.text and m.text.startswith("زوجني "))
    def marry_by_id(message: Message):
        chat_id = message.chat.id
        user = message.from_user

        try:
            target_id = int(message.text.split()[1])
            partner = bot.get_chat_member(chat_id, target_id).user
        except:
            bot.reply_to(message, "⚠️ اكتب الايدي صح")
            return

        if partner.is_bot:
            bot.reply_to(message, "🤖 البوتات ما تتزوج")
            return

        if db_marriage.is_married(chat_id, user.id) or db_marriage.is_married(chat_id, partner.id):
            bot.reply_to(message, "😅 أحدكم متزوج")
            return

        db_marriage.marry(chat_id, user.id, partner.id)
        percent = db_marriage.marriages[chat_id][user.id]["love_percent"]
        dowry = db_marriage.marriages[chat_id][user.id]["dowry"]

        bot.send_photo(chat_id, MARRIAGE_IMAGE, caption=f"""
💍 زواج بالإيدي

🤵 {user.first_name}
👰 {partner.first_name}

💸 المهر: {dowry} ذهب
{love_text(percent)}
""")

    # ======================
    # طلقني
    # ======================
    @bot.message_handler(func=lambda m: m.text == "طلقني")
    def divorce(message: Message):
        chat_id = message.chat.id
        user = message.from_user

        if not db_marriage.is_married(chat_id, user.id):
            bot.reply_to(message, "😐 انت مو متزوج")
            return

        db_marriage.divorce(chat_id, user.id)
        bot.reply_to(message, "💔 تم الطلاق… الدنيا قاسية 😂")

    # ======================
    # المتزوجين
    # ======================
    @bot.message_handler(func=lambda m: m.text == "المتزوجين")
    def list_married(message: Message):
        chat_id = message.chat.id
        data = db_marriage.get_all_married(chat_id)

        if not data:
            bot.reply_to(message, "😐 ماكو متزوجين")
            return

        text = "💍 قائمة المتزوجين:\n\n"
        for u, p, percent, dowry in data:
            u_name = bot.get_chat_member(chat_id, u).user.first_name
            p_name = bot.get_chat_member(chat_id, p).user.first_name
            text += f"🤵 {u_name} × 👰 {p_name} | مهر: {dowry} | حب: {percent}%\n"

        bot.send_message(chat_id, text)
