from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# الدالة التي تنفذ عند كتابة /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا العقل المدبر.. تم تفعيل الربط التلقائي بنجاح ✅")

# ملاحظة: يجب أن يكون اسم المتغير 'handler' لكي يتعرف عليه ملف main.py
handler = CommandHandler("start", start_command)
