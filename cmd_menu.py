from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التحقق من أن النص المرسل هو كلمة "اوامر"
    if update.message.text == "اوامر":
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

# تغيير نوع الـ handler من CommandHandler إلى MessageHandler لكي يقرأ الكلمات العادية
handler = MessageHandler(filters.TEXT & (~filters.COMMAND), menu_text_handler)
