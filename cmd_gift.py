import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import db_manager

# الذاكرة المؤقتة للوقت
last_gift_time = {}

async def gift_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التحقق من وجود رسالة
    if not update.message: return
    
    user_id = update.message.from_user.id
    now = datetime.now()

    # 1. فحص الوقت (24 ساعة)
    if user_id in last_gift_time:
        time_diff = now - last_gift_time[user_id]
        if time_diff < timedelta(hours=24):
            remaining = timedelta(hours=24) - time_diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            await update.message.reply_text(f"⏳ هديتك القادمة بعد {hours} ساعة و {minutes} دقيقة.")
            return

    # 2. تحديث البيانات
    data = db_manager.load_data()
    user = db_manager.get_user(user_id)
    
    gift_points = random.randint(50, 300)
    user["points"] += gift_points
    
    # حفظ البيانات
    data[str(user_id)] = user
    db_manager.save_data(data)
    last_gift_time[user_id] = now
    
    await update.message.reply_text(f"🎁 مبروك! حصلت على {gift_points} نقطة.\n💰 رصيدك الآن: {user['points']}")

# تأكد أن الاسم ينتهي بـ _handler (ليتم تحميله تلقائياً)
gift_main_handler = CommandHandler("gift", gift_command)
