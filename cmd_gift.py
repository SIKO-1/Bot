import random
from datetime import datetime
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
import db_manager

async def gift_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_msg = update.message.text.strip()
    
    if user_msg == "هدية":
        user_id = update.message.from_user.id
        data = db_manager.load_data()
        user = db_manager.get_user(user_id)
        
        # وقتنا الحالي
        now = datetime.now()
        
        # التحقق من وقت آخر هدية محفوظ في بيانات المستخدم
        last_gift_str = user.get("last_gift_time")
        
        if last_gift_str:
            last_gift = datetime.fromisoformat(last_gift_str)
            # حساب الفرق (هل مرت 24 ساعة؟)
            diff = now - last_gift
            if diff.total_seconds() < 24 * 3600:
                remaining = 24 * 3600 - diff.total_seconds()
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                await update.message.reply_text(f"⏳ طماع! باقي لك {hours} ساعة و {minutes} دقيقة على هديتك الجاية.")
                return

        # إذا مرت 24 ساعة أو أول مرة يأخذ هدية:
        points_win = random.randint(50, 300)
        user["points"] += points_win
        # حفظ الوقت الحالي بصيغة نصية داخل الـ JSON
        user["last_gift_time"] = now.isoformat()
        
        # حفظ كل البيانات
        data[str(user_id)] = user
        db_manager.save_data(data)
        
        await update.message.reply_text(
            f"🎁 **أبشر بالهدية!**\n"
            f"━━━━━━━━━━━━━\n"
            f"💰 ربحت: {points_win} نقطة\n"
            f"🏦 رصيدك الكلي: {user['points']}\n"
            f"━━━━━━━━━━━━━\n"
            f"📅 تعال باكر في نفس الوقت!"
        )

gift_arabic_handler = MessageHandler(filters.Text(["هدية"]), gift_text_handler)
