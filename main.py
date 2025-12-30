import os
import random
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

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

# ================== XO ==================
xo_games = {}

def draw(board):
    return f"""
{board[0]}|{board[1]}|{board[2]}
-----
{board[3]}|{board[4]}|{board[5]}
-----
{board[6]}|{board[7]}|{board[8]}
"""

# ================== الأوامر ==================
@bot.message_handler(commands=['start'])
def start(message):
    u = get_user(message.from_user)
    bot.send_message(message.chat.id, f"👋 هلا {u['name']}\nبوت ألعاب مجنون 🎮🔥\nاكتب: اوامر")

@bot.message_handler(func=lambda m: m.text == "اوامر")
def commands_list(message):
    bot.send_message(message.chat.id, "📜 الأوامر:\nايدي\nالعاب\nمتجر\nxo\nاسئلة\nصح")

@bot.message_handler(func=lambda m: m.text == "ايدي")
def user_info(message):
    u = get_user(message.from_user)
    bot.send_message(message.chat.id, f"👤 {u['name']}\n⭐ المستوى: {u['level']}\n🎯 النقاط: {u['points']}\n💰 الفلوس: {u['money']}\n🎮 الألعاب: {', '.join(u['games'])}")

@bot.message_handler(func=lambda m: m.text == "العاب")
def games_list(message):
    u = get_user(message.from_user)
    bot.send_message(message.chat.id, "🎮 ألعابك:\n" + "\n".join(u["games"]))

@bot.message_handler(func=lambda m: m.text == "متجر")
def shop_list(message):
    text = "🛒 المتجر:\n"
    for g, p in shop_games.items():
        text += f"{g} - {p} نقطة\n"
    text += "\nللشراء: كتابة 'شراء اسم_اللعبة'"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text.startswith("شراء "))
def buy_game(message):
    u = get_user(message.from_user)
    parts = message.text.split()
    if len(parts) < 2:
        return
    game = parts[1]
    if game not in shop_games:
        bot.send_message(message.chat.id, "❌ لعبة غير موجودة")
        return
    if game in u["games"]:
        bot.send_message(message.chat.id, "⚠️ اللعبة مفتوحة")
        return
    price = shop_games[game]
    if u["money"] < price:
        bot.send_message(message.chat.id, "💔 نقاطك ما تكفي")
        return
    u["money"] -= price
    u["games"].append(game)
    bot.send_message(message.chat.id, f"✅ اشتريت {game}")

# ================== أسئلة ==================
@bot.message_handler(func=lambda m: m.text == "اسئلة")
def quiz_start(message):
    q = random.choice(quiz_questions)
    users[message.from_user.id]["quiz"] = q
    text = f"❓ {q['q']}\n"
    for i, o in enumerate(q["opts"]):
        text += f"{i+1}- {o}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text in ["1","2","3"])
def quiz_answer(message):
    user_data = users.get(message.from_user.id, {})
    if "quiz" not in user_data:
        return
    try:
        ans = int(message.text)-1
    except:
        return
    q = user_data["quiz"]
    if ans == q["a"]:
        add_points(message.from_user.id, 3)
        bot.send_message(message.chat.id, "✅ صحيح +3")
    else:
        bot.send_message(message.chat.id, "❌ خطأ")
    del user_data["quiz"]

# ================== صح / خطأ ==================
@bot.message_handler(func=lambda m: m.text == "صح")
def tf_true(message):
    tf_answer_func(message, True)

@bot.message_handler(func=lambda m: m.text == "خطأ")
def tf_false(message):
    tf_answer_func(message, False)

def tf_answer_func(message, answer):
    user_data = users.get(message.from_user.id, {})
    if "tf" not in user_data:
        q, correct = random.choice(tf_questions)
        user_data["tf"] = (q, correct)
        bot.send_message(message.chat.id, f"❓ {q}\nصح / خطأ")
        return
    q, correct = user_data["tf"]
    if answer == correct:
        add_points(message.from_user.id, 3)
        bot.send_message(message.chat.id, "✅ صح +3")
    else:
        bot.send_message(message.chat.id, "❌ خطأ")
    del user_data["tf"]

# ================== XO ==================
@bot.message_handler(func=lambda m: m.text == "xo")
def xo_start(message):
    xo_games[message.from_user.id] = [" "]*9
    bot.send_message(message.chat.id, "🎮 XO ضد البوت\nاكتب رقم من 1 إلى 9")

@bot.message_handler(func=lambda m: m.text.isdigit() and 1 <= int(m.text) <= 9)
def xo_move(message):
    if message.from_user.id not in xo_games:
        return
    board = xo_games[message.from_user.id]
    move = int(message.text)-1
    if board[move] != " ":
        return
    board[move] = "X"
    free = [i for i,v in enumerate(board) if v==" "]
    if free:
        board[random.choice(free)] = "O"
    bot.send_message(message.chat.id, draw(board))

# ================== تشغيل البوت ==================
print("🔥 BOT IS RUNNING 🔥")
bot.infinity_polling()
