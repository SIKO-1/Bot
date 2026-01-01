from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التأكد من استلام كلمة "اوامر"
    if update.message and update.message.text and update.message.text.strip() == "اوامر":
        menu_text = (
            "```\n"
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
            "╚══════════════════════════╝\n"
            "```\n"
            "✦ اكتب الأمر المطلوب للبدء ✦"
        )
        
        await update.message.reply_text(menu_text, parse_mode='MarkdownV2')

# تصدير الهاندلر لـ main.py
show_menu_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), menu_text_handler)
