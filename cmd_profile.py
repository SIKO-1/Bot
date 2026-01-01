from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
import db_manager

async def master_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user_id = update.message.from_user.id
    msg_text = update.message.text.strip()
    
    # زيادة الخبرة للرسائل العادية
    if not msg_text.startswith('/'):
        user = db_manager.get_user(user_id)
        data = db_manager.load_data()
        user["exp"] += 1
        if user["exp"] >= 2: # للتجربة مستوى كل رسالتين
            user["level"] += 1
            user["exp"] = 0
            user["points"] += 25
            await update.message.reply_text(f"🆙 كفو! صعدت للمستوى {user['level']}")
        data[str(user_id)] = user
        db_manager.save_data(data)

    # الرد على أمر مستوى
    if msg_text in ["مستوى", "رتبتي"]:
        user = db_manager.get_user(user_id)
        response = (
            "📊 **معلوماتك الإمبراطورية**\n"
            "━━━━━━━━━━━━━\n"
            f"👤 الأسم: {update.message.from_user.first_name}\n"
            f"🎖 الرتبة: {user['rank']}\n"
            f"🆙 المستوى: {user['level']}\n"
            f"💰 النقاط: {user['points']}\n"
            "━━━━━━━━━━━━━"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

# تأكد أن هذا السطر في نهاية الملف تماماً
system_master_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), master_handler)
