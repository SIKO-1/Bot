import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import db_manager

# قاموس لحفظ وقت آخر هدية (سيتم تصفيره عند إعادة تشغيل البوت، للدوام الكامل يفضل حفظه في JSON)
last_gift_time = {}

async def gift_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    now = datetime.now()

    # التحقق مما إذا كان المستخدم قد أخذ الهدية خلال آخر 24 ساعة
    if user_id in last_gift_time:
        time_diff = now - last_gift_time[user_id]
        if time_diff < timedelta(hours=24):
            remaining = timedelta(hours=24) - time_diff
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            await update.message.reply_text(f"⚠️ لقد استلمت هديتك بالفعل! عد بعد {hours} ساعة و {minutes} دقيقة.")
            return

    # توليد نقاط عشوائية بين 50 و 300
    gift_points = random.randint(50, 300)
    
    # تحديث بيانات المستخدم
    data = db_manager.load_data()
    user = db_manager.get_user(user_id)
    user["points"] += gift_points
    db_manager.save_data(data)
    
    # تسجيل وقت الاستلام
    last_gift_time[user_id] = now
    
    response = (
        f"🎁 **مبروك! لقد حصلت على هدية إمبراطورية**\n"
        f"━━━━━━━━━━━━━\n"
        f"💰 النقاط المكتسبة: {gift_points}\n"
        f"🏦 رصيدك الإجمالي الآن: {user['points']}\n"
        f"━━━━━━━━━━━━━\n"
        f"✨ يمكنك العودة للحصول على هدية أخرى بعد 24 ساعة."
    )
    await update.message.reply_text(response, parse_mode='Markdown')

# هاندلر الأمر
gift_handler = CommandHandler("gift", gift_command)
