from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # نستخدم strip() لإزالة أي مسافات زائدة
    if update.message and update.message.text and update.message.text.strip() == "اوامر":
        menu_text = (
            "┏━━━━━━━━━━━━━━━━━━━━┓\n"
            "┃      ⚜️ إمبراطورية كرار ⚜️     ┃\n"
            "┣━━━━━━━━━━━━━━━━━━━━┫\n"
            "┃  🔹 العاب                      ┃\n"
            "┃  🔹 مستوى                    ┃\n"
            "┃  🔹 الامبراطورية             ┃\n"
            "┗━━━━━━━━━━━━━━━━━━━━┛\n"
            "✦ اكتب الأمر المطلوب للبدء ✦"
        )
        await update.message.reply_text(menu_text)

# تأكد أن الاسم ينتهي بـ _handler لكي يقرأه ملف main.py الجديد
show_menu_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), menu_text_handler)
