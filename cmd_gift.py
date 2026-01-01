import random
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
import db_manager

async def gift_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التأكد من وجود رسالة نصية
    if not update.message or not update.message.text:
        return
    
    user_msg = update.message.text.strip()
    
    # الرد فقط إذا كانت الكلمة هي "هدية"
    if user_msg == "هدية":
        user_id = update.message.from_user.id
        
        # تحميل البيانات
        data = db_manager.load_data()
        user = db_manager.get_user(user_id)
        
        # توليد نقاط عشوائية (حد أقصى 300)
        points_win = random.randint(50, 300)
        user["points"] += points_win
        
        # حفظ البيانات
        data[str(user_id)] = user
        db_manager.save_data(data)
        
        response = (
            f"🎁 **أبشر بالخير! هذي هديتك:**\n"
            f"━━━━━━━━━━━━━\n"
            f"💰 ربحت: {points_win} نقطة\n"
            f"🏦 رصيدك الآن: {user['points']}\n"
            f"━━━━━━━━━━━━━"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

# الهاندلر الذي يراقب كلمة "هدية" حصراً
gift_arabic_handler = MessageHandler(filters.Text(["هدية"]), gift_text_handler)
