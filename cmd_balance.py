from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
import db_manager

async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    msg = update.message.text.strip()
    user_id = update.message.from_user.id
    user = db_manager.get_user(user_id)

    # إذا كتب "رصيد"
    if msg == "رصيد":
        await update.message.reply_text(f"💰 رصيدك الحالي: {user['points']} نقطة.")
    
    # إذا كتب "مستوى"
    elif msg in ["مستوى", "رتبتي"]:
        response = (
            f"👤 الأسم: {update.message.from_user.first_name}\n"
            f"🎖 الرتبة: {user['rank']}\n"
            f"🆙 المستوى: {user['level']}\n"
            f"💰 النقاط: {user['points']}"
        )
        await update.message.reply_text(response)

# هذا الهاندلر سيعمل في "المجموعة 0" لضمان السرعة
check_stats_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), stats_handler)
