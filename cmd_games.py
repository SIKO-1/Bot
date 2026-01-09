# cmd_games.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

COMMANDS = ["الالعاب", "العاب", "لعبات"]

def handle(bot, message):
    if message.text not in COMMANDS:
        return

    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("🧠 ذكاء", callback_data="games_brain"),
        InlineKeyboardButton("🎲 حظ", callback_data="games_luck"),
        InlineKeyboardButton("💬 كلام", callback_data="games_talk"),
        InlineKeyboardButton("🔥 تحديات", callback_data="games_challenge"),
        InlineKeyboardButton("🌍 معلومات", callback_data="games_info"),
        InlineKeyboardButton("🎮 متنوعة", callback_data="games_misc"),
    )

    text = f"""
╔═════════════════╗
    الألعاب الإمبراطورية
╚═════════════════╝

مرحباً بك يا {message.from_user.first_name} 👑
━━━━━━━━━━━━━━━
اختر القسم:
"""

    bot.send_message(message.chat.id, text, reply_markup=kb)


def register_callbacks(bot):

    @bot.callback_query_handler(func=lambda call: call.data.startswith("games_"))
    def games_sections(call):

        sections = {
            "games_brain": """🧠 ألعاب الذكاء:
• لغز
• حزورة
• المختلف
• ترتيب
• نشط عقلك
• المليون
• رياضيات""",

            "games_luck": """🎲 ألعاب الحظ:
• نرد
• روليت
• الحظ
• حظي
• ارقام""",

            "games_talk": """💬 ألعاب الكلام:
• صراحة
• لو خيروك
• كت تويت
• اسالني
• امثله""",

            "games_challenge": """🔥 التحديات:
• تحدي
• XO
• بات""",

            "games_info": """🌍 المعلومات:
• معاني
• اعلام
• عواصم
• مقالات
• انكليزي""",

            "games_misc": """🎮 ألعاب متنوعة:
• اغاني
• كلمات
• سمايلات
• خمن"""
        }

        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, sections.get(call.data, "❌ قسم غير معروف"))
