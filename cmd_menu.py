from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # نتحقق من الكلمة بدقة
    if update.message and update.message.text:
        user_msg = update.message.text.strip()
        if user_msg == "اوامر":
            menu_text = (
                "⚜️ إمبراطورية كرار ⚜️\n"
                "━━━━━━━━━━━━━\n"
                "🎮 العاب\n"
                "🆙 مستوى\n"
                "🏛 الامبراطورية\n"
                "━━━━━━━━━━━━━\n"
                "✦ اكتب الأمر المطلوب للبدء ✦"
            )
            await update.message.reply_text(menu_text)

# التأكد من التسمية الصحيحة ليتعرف عليها العقل
show_menu_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), menu_text_handler)
