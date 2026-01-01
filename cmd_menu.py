from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # نص القائمة بالتنسيق الذي طلبته
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
    
    # إرسال الرسالة مع تفعيل خاصية الـ MarkdownV2 لتظهر الخطوط متناسقة
    await update.message.reply_text(menu_text, parse_mode='MarkdownV2')

# العقل سيتعرف عليه تلقائياً
handler = CommandHandler("menu", menu_command)
