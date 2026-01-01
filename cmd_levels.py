from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
import db_manager # استدعاء ملف الذاكرة الذي أضفته

async def experience_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تجاهل الأوامر (التي تبدأ بـ /) والرسائل غير النصية
    if not update.message or not update.message.text or update.message.text.startswith('/'):
        return

    user_id = update.message.from_user.id
    data = db_manager.load_data()
    user = db_manager.get_user(user_id)

    # زيادة الخبرة (EXP)
    user["exp"] += 1
    
    # الصعود للمستوى التالي (يحتاج المستوى الحالي * 5 رسائل)
    needed_exp = user["level"] * 5
    
    if user["exp"] >= needed_exp:
        user["level"] += 1
        user["exp"] = 0
        user["points"] += 25 # مكافأة النقاط
        await update.message.reply_text(f"🎊 كفو! صعدت للمستوى {user['level']} وحصلت على 25 نقطة!")

    # حفظ البيانات المحدثة
    data[str(user_id)] = user
    db_manager.save_data(data)

# تصدير الهاندلر ليعرفه ملف main.py
level_system_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), experience_handler)
