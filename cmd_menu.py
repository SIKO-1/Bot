from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # نتحقق إذا كانت الرسالة نصية
    if update.message and update.message.text:
        user_msg = update.message.text.strip()
        
        # سيتعرف على "اوامر" أو "الأوامر" أو "الاوامر"
        if user_msg in ["اوامر", "الاوامر", "الأوامر", "أوامر"]:
            menu_text = (
                "⚜️ **إمبراطورية كرار** ⚜️\n"
                "━━━━━━━━━━━━━\n"
                "🎮 **العاب**\n"
                "🆙 **مستوى**\n"
                "🏛 **الامبراطورية**\n"
                "━━━━━━━━━━━━━\n"
                "✦ اكتب الأمر المطلوب للبدء ✦"
            )
            # نستخدم Markdown العادي (بدون V2) لتجنب الأخطاء البرمجية
            await update.message.reply_text(menu_text, parse_mode='Markdown')

# تأكد أن اسم المتغير ينتهي بـ _handler
menu_display_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), menu_text_handler)
