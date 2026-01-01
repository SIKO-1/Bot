from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
import db_manager

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    text = update.message.text.strip()
    # الرد على الكلمات التالية
    if text in ["مستوى", "رتبتي", "المستوى"]:
        user = db_manager.get_user(update.message.from_user.id)
        
        msg = (
            "📊 **بطاقتك الإمبراطورية**\n"
            "━━━━━━━━━━━━━\n"
            f"👤 الأسم: {update.message.from_user.first_name}\n"
            f"🎖 الرتبة: {user['rank']}\n"
            f"🆙 المستوى: {user['level']}\n"
            f"💰 النقاط: {user['points']}\n"
            "━━━━━━━━━━━━━"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

# التأكد من انتهاء الاسم بـ _handler لكي يقرأه ملف main.py عندك
profile_info_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), profile_handler)
