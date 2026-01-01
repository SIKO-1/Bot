from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import db_manager

# قائمة الرتب والأسعار
RANKS = [
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
    
    if not context.args:
        await update.message.reply_text("❌ اكتب اسم الرتبة بعد الأمر. مثال: `/buy متدرب`", parse_mode='Markdown')
        return
    
    target_rank_name = " ".join(context.args)
    current_rank = user['rank']
    
    # تحديد موقع الرتبة الحالية والمطلوبة
    current_idx = next((i for i, r in enumerate(RANKS) if r[0] == current_rank), 0)
    target_info = next(((i, r) for i, r in enumerate(RANKS) if r[0] == target_rank_name), None)

    if not target_info:
        await update.message.reply_text("❌ هذه الرتبة غير موجودة في السوق!")
        return

    target_idx, (name, price) = target_info

    if target_idx <= current_idx:
        await update.message.reply_text("❌ أنت بالفعل في هذه الرتبة أو أعلى!")
    elif target_idx > current_idx + 1:
        await update.message.reply_text(f"⚠️ لا يمكنك القفز! يجب شراء رتبة ({RANKS[current_idx+1][0]}) أولاً.")
    elif user['points'] < price:
        await update.message.reply_text(f"💰 نقاطك ({user['points']}) لا تكفي. سعر الرتبة: {price}")
    else:
        user['points'] -= price
        user['rank'] = name
        data[str(user_id)] = user
        db_manager.save_data(data)
        await update.message.reply_text(f"🎊 مبروك! تمت ترقيتك إلى رتبة **{name}**")

buy_rank_handler = CommandHandler("buy", buy_rank)
