from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
import db_manager

async def master_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user_id = update.message.from_user.id
    msg_text = update.message.text.strip()
    
    # 1. تحديث البيانات وزيادة الخبرة مع كل رسالة (ما عدا الأوامر)
    if not msg_text.startswith('/'):
        data = db_manager.load_data()
        user = db_manager.get_user(user_id)
        
        user["exp"] += 1
        # صعود سريع جداً للتجربة (كل رسالتين مستوى)
        if user["exp"] >= 2:
            user["level"] += 1
            user["exp"] = 0
            user["points"] += 25
            await update.message.reply_text(f"🆙 كفو! صعدت للمستوى {user['level']}")
        
        data[str(user_id)] = user
        db_manager.save_data(data)

    # 2. الرد على أمر مستوى أو رتبتي فوراً
    if msg_text in ["مستوى", "رتبتي", "المستوى"]:
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

# هذا الهاندلر سيراقب كل شيء (النصوص والأوامر النصية)
system_master_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), master_handler)
