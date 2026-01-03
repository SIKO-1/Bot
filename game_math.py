import random
import time
from telebot import types
import db_manager # الربط بالخزنة الملكية

def register_handlers(bot):
    active_math_challenges = {}

    @bot.message_handler(func=lambda m: m.text == "رياضيات")
    def start_math_game(m):
        chat_id = m.chat.id
        
        # توليد مسألة عشوائية
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
            "💰 الـجـائـزة : 50 ذهبة"
        )
        bot.send_message(chat_id, text)

    @bot.message_handler(func=lambda m: m.chat.id in active_math_challenges)
    def check_math_answer(m):
        chat_id = m.chat.id
        challenge = active_math_challenges[chat_id]
        
        # إذا كانت الإجابة صحيحة
        if m.text == challenge["answer"]:
            elapsed = round(time.time() - challenge["start_time"], 2)
            
            if elapsed <= 15:
                uid = m.from_user.id
                # إضافة الذهب للخزنة الحقيقية
                db_manager.update_user_gold(uid, 50)
                
                win_text = (
                    "⌯ تـم الـتـحـقـق مـن الإجـابـة ⌯\n"
                    "━━━━━━━━━━━━━━\n"
                    f"👤 الـفـائـز : {m.from_user.first_name}\n"
                    f"⚡ الـزمـن : {elapsed} ثانية\n"
                    "✅ الإجـابـة : صـحـيـحـة (يا عبقري)\n"
                    "💰 الـجـوائـز : +50 ذهـبـة"
                )
                bot.reply_to(m, win_text)
                del active_math_challenges[chat_id] # إنهاء التحدي فوراً
            else:
                bot.reply_to(m, f"🐢 إجابة صحيحة ولكنك بطيء! استغرقت {elapsed} ثانية.. انتهى الوقت.")
                del active_math_challenges[chat_id]
        
        # إذا كانت الإجابة خاطئة لا نحذف التحدي لنعطي فرصة لغيره، 
        # إلا إذا انتهى الوقت (اختياري)
