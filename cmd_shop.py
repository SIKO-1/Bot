from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import db_manager

# قائمة الرتب مع أسعارها مرتبة
RANKS_DATA = [
    ("مبتدئ", 0), ("متدرب", 250), ("حارس", 500), ("جندي", 650), ("فارس", 900),
    ("محارب", 1100), ("قائد وحدة", 1300), ("ظابط", 1500), ("مشرف", 1700),
    ("فنان القتال", 2000), ("نقيب", 2300), ("رائد", 2600), ("أمير", 2900),
    ("قائد النخبة", 3300), ("حاكم الإقليم", 3700), ("سليل الدم", 4200),
    ("سيد الظل", 4600), ("مستشار الإمبراطور", 5000), ("حامي العرش", 5500),
    ("فارس الأساطير", 6100), ("نجم الحرب", 6700), ("سيد القوة", 7400),
    ("الحاكم الأعلى", 8200), ("ولي العهد", 9000)
]

async def buy_rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    data = db_manager.load_data()
    user = db_manager.get_user(user_id)
    
    # الحصول على نص الرتبة المطلوب شراؤها
    if not context.args:
        await update.message.reply_text("❌ يرجى كتابة اسم الرتبة بعد الأمر. مثال: /buy متدرب")
        return
    
    requested_rank = " ".join(context.args)
    
    # البحث عن ترتيب الرتبة الحالية والمطلوبة
    current_index = next((i for i, r in enumerate(RANKS_DATA) if r[0] == user['rank']), 0)
    target_rank_info = next(((i, r) for i, r in enumerate(RANKS_DATA) if r[0] == requested_rank), None)

    if not target_rank_info:
        await update.message.reply_text("❌ هذه الرتبة غير موجودة في السوق!")
        return

    target_index, (rank_name, price) = target_rank_info

    # التحقق من الشروط
    if target_index <= current_index:
        await update.message.reply_text("❌ أنت بالفعل في هذه الرتبة أو أعلى!")
    elif target_index > current_index + 1:
        await update.message.reply_text(f"⚠️ لا يمكنك القفز! يجب أن تشتري رتبة ({RANKS_DATA[current_index+1][0]}) أولاً.")
    elif user['points'] < price:
        await update.message.reply_text(f"💰 نقاطك لا تكفي! تحتاج إلى {price} نقطة.")
    else:
        # إتمام عملية الشراء
        user['points'] -= price
        user['rank'] = rank_name
        data[str(user_id)] = user
        db_manager.save_data(data)
        await update.message.reply_text(f"🎊 مبروك! تمت ترقيتك إلى رتبة **{rank_name}** بنجاح.")

# تصدير الهاندلر
buy_rank_handler = CommandHandler("buy", buy_rank)
