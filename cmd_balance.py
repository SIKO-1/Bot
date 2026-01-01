from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
import db_manager

async def balance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التأكد من وجود رسالة نصية
    if not update.message or not update.message.text:
        return
    
    msg_text = update.message.text.strip()
    
    # الرد فقط عند كتابة كلمة "رصيد"
    if msg_text == "رصيد":
        user_id = update.message.from_user.id
        user = db_manager.get_user(user_id)
        
        points = user.get("points", 0)
        await update.message.reply_text(f"💰 رصيدك الحالي: {points} نقطة.")

# التأكد من أن الاسم ينتهي بـ _handler ليقرأه ملف main.py
check_balance_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), balance_handler)
