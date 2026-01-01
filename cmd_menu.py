from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_msg = update.message.text.strip()

    # الرد فقط وفقط إذا كانت الكلمة هي "اوامر"
    if user_msg in ["اوامر", "الأوامر", "الاوامر"]:
        menu_text = (
            "⚜️ **إمبراطورية كرار** ⚜️\n"
            "━━━━━━━━━━━━━\n"
            "💰 رصيد (لمعرفة نقاطك)\n"
            "🆙 مستوى (لمعرفة رتبتك)\n"
            "🎮 العاب\n"
            "━━━━━━━━━━━━━"
        )
        await update.message.reply_text(menu_text, parse_mode='Markdown')
    
    # ملاحظة: لم نضع 'else' هنا، لكي نترك المجال للملفات الأخرى أن تعمل

# تعديل الفلتر ليكون دقيقاً جداً
menu_display_handler = MessageHandler(filters.Text(["اوامر", "الأوامر", "الاوامر"]), menu_text_handler)
