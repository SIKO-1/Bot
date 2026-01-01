from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "اوامر":
        await update.message.reply_text("✅ تم استلام الأمر! الإمبراطورية تعمل.")

# تأكد أن الاسم ينتهي بـ _handler
menu_display_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), menu_handler)
