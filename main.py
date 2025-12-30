import os
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

# ================== قاعدة البيانات ==================
users = {}

def get_user(user):
    if user.id not in users:
        users[user.id] = {
            "name": user.first_name,
            "points": 0,
            "money": 0,
            "level": 1,
            "games": ["xo", "quiz", "tf"]
        }
    return users[user.id]

def add_points(user_id, pts):
    u = users[user_id]
    u["points"] += pts
    u["money"] += pts
    u["level"] = min(999, u["points"] // 50 + 1)

# ================== الأسئلة ==================
quiz_questions = [
    {"q": "من هو أول نبي؟", "opts": ["نوح", "آدم", "إبراهيم"], "a": 1},
    {"q": "عاصمة العراق؟", "opts": ["بغداد", "البصرة", "الموصل"], "a": 0},
    {"q": "من قال أنا أفكر إذن أنا موجود؟", "opts": ["سقراط", "ديكارت", "أفلاطون"], "a": 1},
    {"q": "أكبر قارة؟", "opts": ["آسيا", "أفريقيا", "أوروبا"], "a": 0},
    {"q": "الفلسفة تعني؟", "opts": ["حب الحكمة", "حب المال", "حب القوة"], "a": 0},
]

tf_questions = [
    ("الأرض كروية", True),
    ("أرسطو عربي", False),
    ("بغداد مدينة تاريخية", True),
    ("الشمس تدور حول الأرض", False),
    ("المنطق جزء من الفلسفة", True),
]

# ================== المتجر ==================
shop_games = {
    "dice": 30,
    "guess": 40,
    "math": 50,
    "memory": 60,
}

# ================== أوامر ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = get_user(update.effective_user)
    await update.message.reply_text(
        f"👋 هلا {u['name']}\n"
        "بوت ألعاب مجنون 🎮🔥\n\n"
        "اكتب: اوامر"
    )

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 الأوامر:\n"
        "ايدي\n"
        "العاب\n"
        "متجر\n"
        "xo\n"
        "اسئلة\n"
        "صح\n"
    )

async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = get_user(update.effective_user)
    await update.message.reply_text(
        f"👤 {u['name']}\n"
        f"⭐ المستوى: {u['level']}\n"
        f"🎯 النقاط: {u['points']}\n"
        f"💰 الفلوس: {u['money']}\n"
        f"🎮 الألعاب: {', '.join(u['games'])}"
    )

async def games_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = get_user(update.effective_user)
    await update.message.reply_text(
        "🎮 ألعابك:\n" + "\n".join(u["games"])
    )

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🛒 المتجر:\n"
    for g, p in shop_games.items():
        text += f"{g} - {p} نقطة\n"
    text += "\nللشراء: شراء اسم_اللعبة"
    await update.message.reply_text(text)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = get_user(update.effective_user)
    parts = update.message.text.split()
    if len(parts) < 2:
        return
    game = parts[1]
    if game not in shop_games:
        await update.message.reply_text("❌ لعبة غير موجودة")
        return
    if game in u["games"]:
        await update.message.reply_text("⚠️ اللعبة مفتوحة")
        return
    price = shop_games[game]
    if u["money"] < price:
        await update.message.reply_text("💔 نقاطك ما تكفي")
        return
    u["money"] -= price
    u["games"].append(game)
    await update.message.reply_text(f"✅ اشتريت {game}")

# ================== لعبة الأسئلة ==================
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(quiz_questions)
    context.user_data["quiz"] = q
    text = f"❓ {q['q']}\n"
    for i, o in enumerate(q["opts"]):
        text += f"{i+1}- {o}\n"
    await update.message.reply_text(text)

async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "quiz" not in context.user_data:
        return
    try:
        ans = int(update.message.text) - 1
    except:
        return
    q = context.user_data["quiz"]
    if ans == q["a"]:
        add_points(update.effective_user.id, 3)
        await update.message.reply_text("✅ صحيح +3")
    else:
        await update.message.reply_text("❌ خطأ")
    del context.user_data["quiz"]

# ================== صح / خطأ ==================
async def tf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(tf_questions)
    context.user_data["tf"] = q
    await update.message.reply_text(f"❓ {q[0]}\nصح / خطأ")

async def tf_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "tf" not in context.user_data:
        return
    q, correct = context.user_data["tf"]
    user_ans = update.message.text == "صح"
    if user_ans == correct:
        add_points(update.effective_user.id, 3)
        await update.message.reply_text("✅ صح +3")
    else:
        await update.message.reply_text("❌ خطأ")
    del context.user_data["tf"]

# ================== XO ضد البوت ==================
async def xo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    board = [" "] * 9
    context.user_data["xo"] = board
    await update.message.reply_text("🎮 XO\nاختر رقم 1-9")

def draw(board):
    return f"""
{board[0]}|{board[1]}|{board[2]}
-----
{board[3]}|{board[4]}|{board[5]}
-----
{board[6]}|{board[7]}|{board[8]}
"""

async def xo_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "xo" not in context.user_data:
        return
    try:
        m = int(update.message.text) - 1
    except:
        return
    b = context.user_data["xo"]
    if b[m] != " ":
        return
    b[m] = "X"
    free = [i for i in range(9) if b[i] == " "]
    if free:
        b[random.choice(free)] = "O"
    await update.message.reply_text(draw(b))

# ================== تشغيل ==================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^اوامر$"), commands))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^ايدي$"), user_info))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^العاب$"), games_list))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^متجر$"), shop))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^شراء "), buy))

app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^اسئلة$"), quiz))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^[1-3]$"), quiz_answer))

app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^صح$|^خطأ$"), tf_answer))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^صح$|^خطأ$"), tf))

app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^xo$"), xo))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^[1-9]$"), xo_move))

print("🔥 BOT IS RUNNING 🔥")
app.run_polling()
