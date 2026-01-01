from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # نستخدم strip() للتأكد من قراءة الكلمة حتى لو وجد مسافات
    if update.message and update.message.text and update.message.text.strip() == "اوامر":
        menu_text = (
            "╔══════════════════════════╗\n"
            "║      ⚜️ إمبراطورية كرار ⚜️     ║\n"
            "╠══════════════════════════╣\n"
            "║ ┌────────────────────┐ ║\n"
            "║ │        العاب        │ ║\n"
            "║ ├────────────────────┤ ║\n"
            "║ │        مستوى        │ ║\n"
            "║ ├────────────────────┤ ║\n"
            "║ │     الامبراطورية     │ ║\n"
            "║ └────────────────────┘ ║\n"
            "╚══════════════════════════╝\n\n"
            "✦ اكتب الأمر المطلوب للبدء ✦"
        )
        
        await update.message.reply_text(menu_text)

# تأكد أن الاسم ينتهي بـ _handler
show_menu_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), menu_text_handler)
