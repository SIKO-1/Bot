from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import db_manager

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = db_manager.get_user(user_id)
    
    # تنسيق الرسالة بشكل جميل
    response = (
        "📊 **بطاقة معلومات الإمبراطورية**\n"
        "━━━━━━━━━━━━━\n"
        f"👤 الأسم: {update.message.from_user.first_name}\n"
        f"💰 الرصيد: {user['points']} نقطة\n"
        f"🆙 المستوى: {user['level']}\n"
        f"🎖 الرتبة: {user['rank']}\n"
        "━━━━━━━━━━━━━\n"
        "💡 ترقبوا المزيد من المهام قريباً!"
    )
    await update.message.reply_text(response, parse_mode='Markdown')

# هاندلر للأمر /info
# يمكنك إضافة أوامر أخرى هنا مثل /balance بنفس الطريقة
info_handler = CommandHandler("info", info_command)
balance_handler = CommandHandler("رصيدي", info_command) # سيعمل بكلمة /رصيدي أيضاً
