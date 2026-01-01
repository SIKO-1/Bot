from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "اوامر":
        # استخدمنا هنا تنسيقاً يضمن أن كل سطر له نفس العرض برمجياً
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
        
        # إرسالها بنظام التنسيق العادي لضمان عدم تداخل الخطوط
        await update.message.reply_text(menu_text)

handler = MessageHandler(filters.TEXT & (~filters.COMMAND), menu_text_handler)
