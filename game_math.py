import random
import time
from telebot import types

# نظام النقاط المرتبط بالـ Volume
try:
    from db_manager import get_user, update_user
except:
    def get_user(uid): return {"balance": 0}
    def update_user(uid, k, v): pass

def register_handlers(bot):
    active_math_challenges = {}

    @bot.message_handler(func=lambda m: m.text == "رياضيات")
    def start_math_game(m):
        chat_id = m.chat.id
        
        # توليد مسألة عشوائية من بين 50 مستوى صعوبة
        op = random.choice(['+', '-', '*'])
        
        if op == '+':
            n1, n2 = random.randint(10, 100), random.randint(10, 100)
            answer = str(n1 + n2)
            question = f"{n1} + {n2}"
        elif op == '-':
            n1, n2 = random.randint(50, 150), random.randint(10, 50)
            answer = str(n1 - n2)
            question = f"{n1} - {n2}"
        else: # ضرب
            n1, n2 = random.randint(2, 12), random.randint(2, 12)
            answer = str(n1 * n2)
            question = f"{n1} × {n2}"

        active_math_challenges[chat_id] = {
            "answer": answer,
            "start_time": time.time()
        }

        # الزخرفة الإمبراطورية الفخمة
        text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ تـحـدي الـريـاضـيـات ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            f"  » أوجد ناتج العملية : [ {question} ]\n\n"
            "🕒 أمامك 15 ثانية للحل!\n"
            "💰 الـجـائـزة : 50 نـقـطـة"
        )
        bot.send_message(chat_id, text)

    @bot.message_handler(func=lambda m: m.chat.id in active_math_challenges)
    def check_math_answer(m):
        chat_id = m.chat.id
        challenge = active_math_challenges[chat_id]
        
        if m.text == challenge["answer"]:
            elapsed = round(time.time() - challenge["start_time"], 2)
            
            if elapsed <= 15:
                uid = m.from_user.id
                bal = get_user(uid).get("balance", 0)
                update_user(uid, "balance", bal + 50)
                
                win_text = (
                    "⌯ تـم الـتـحـقـق مـن الإجـابـة ⌯\n"
                    "━━━━━━━━━━━━━━\n"
                    f"👤 الـفـائـز : {m.from_user.first_name}\n"
                    f"⚡ الـزمـن : {elapsed} ثانية\n"
                    "✅ الإجـابـة : صـحـيـحـة\n"
                    "💰 الـجـوائـز : +50 نـقـاط"
                )
                bot.reply_to(m, win_text)
            else:
                bot.reply_to(m, f"🐢 إجابة صحيحة ولكنك بطيء! استغرقت {elapsed} ثانية والحد المسموح 15.")
            
            del active_math_challenges[chat_id]
