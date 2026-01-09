# cmd_games_buttons.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

COMMANDS = ["الالعاب", "العاب", "لعبات"]

# قائمة كل الألعاب + وصفها
GAMES = {
    "نرد": "لعبة رمي النرد الإمبراطوري",
    "روليت": "لعبة الروليت الإمبراطوري",
    "المختلف": "لعبة المختلف",
    "امثله": "لعبة الأمثلة",
    "العكس": "لعبة عكس الكلمة",
    "حزوره": "لعبة الحزورة",
    "معاني": "لعبة المعاني",
    "بات": "لعبة البات",
    "خمن": "لعبة التخمين",
    "ترتيب": "لعبة ترتيب الحروف",
    "سمايلات": "لعبة السمايلات",
    "اسئله": "أسئلة منوعة",
    "اسالني": "أسئلة عامة متجددة",
    "لغز": "ألغاز الذكاء المتجددة",
    "رياضيات": "مسائل رياضية",
    "انكليزي": "معاني الكلمات",
    "كت": "أسئلة ترفيهية",
    "كت تويت": "أسئلة ترفيهية",
    "لو خيروك": "لعبة لو خيروك",
    "صراحه": "لعبة الصراحة",
    "اعلام": "لعبة اعلام الدول",
    "مقالات": "لعبة المقالات",
    "عواصم": "لعبة عواصم الدول",
    "كلمات": "لعبة كتابة الكلمات",
    "الحظ": "لعبة الحظ الشفافة",
    "حظي": "لعبة ربح أو خسارة",
    "اغاني": "لعبة اسم الفنان",
    "تحدي": "لعبة صراحة مع تاك عشوائي",
    "XO": "لعبة XO الشفافة",
    "رقم": "لعبة أرقام عشوائية",
    "المليون": "لعبة من سيربح المليون",
    "نشط عقلك": "لعبة أسئلة منوعة"
}

def handle(bot, message):
    if message.text not in COMMANDS:
        return

    kb = InlineKeyboardMarkup(row_width=2)
    for game in GAMES.keys():
        kb.add(InlineKeyboardButton(game, callback_data=f"game_{game}"))

    text = f"""
╔═════════════════╗
      الألعاب الإمبراطورية
╚═════════════════╝

مرحباً بك يا {message.from_user.first_name} 👑
━━━━━━━━━━━━━━━
اضغط على أي لعبة لمعرفة معلوماتها:
"""

    bot.send_message(message.chat.id, text, reply_markup=kb)


def register_callbacks(bot):

    @bot.callback_query_handler(func=lambda call: call.data.startswith("game_"))
    def game_info(call):
        game_name = call.data.replace("game_", "")
        description = GAMES.get(game_name, "❌ معلومات غير موجودة لهذه اللعبة")
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"🎮 {game_name}:\n{description}")
