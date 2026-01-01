import random
import time

def register_handlers(bot):
    # قائمة الكلمات التي أرسلتها أنت (سنستخدمها للتفكيك والترتيب)
    WORDS_DATABASE = [
        "قسطنطينية", "استسقيناكموها", "المتشابهات", "الإسكندرية", "الميتافيزيقيا",
        "الأنثروبولوجيا", "الإيديولوجيات", "الاستشراق", "مستضعفون", "ليستخلفنهم"
    ]

    active_time_challenges = {}

    @bot.message_handler(func=lambda m: m.text == "وقت")
    def start_time_game(m):
        chat_id = m.chat.id
        
        # اختيار نوع التحدي عشوائياً (1: حساب، 2: تفكيك، 3: ترتيب)
        challenge_type = random.randint(1, 3)
        
        if challenge_type == 1:
            # تحدي الحساب
            n1, n2 = random.randint(10, 60), random.randint(5, 30)
            op = random.choice(['+', '-'])
            answer = str(n1 + n2) if op == '+' else str(n1 - n2)
            question = f"أوجد ناتج: {n1} {op} {n2}"
            task_name = "المسائل الحسابية"

        elif challenge_type == 2:
            # تحدي التفكيك (وضع فواصل بين الحروف)
            word = random.choice(WORDS_DATABASE)
            answer = " ".join(list(word))
            question = f"قم بتفكيك كلمة: ({word})"
            task_name = "تفكيك الكلمات"
            # مثال: قسطنطينية -> ق س ط ن ط ي ن ي ة

        else:
            # تحدي ترتيب الحروف
            original_word = random.choice(WORDS_DATABASE)
            shuffled = list(original_word)
            random.shuffle(shuffled)
            answer = original_word
            question = f"رتب الحروف التالية لتكوين كلمة: ({' - '.join(shuffled)})"
            task_name = "ترتيب الحروف"

        active_time_challenges[chat_id] = {
            "answer": answer,
            "start_time": time.time()
        }

        msg = (
            f"⌔︙تحدي الوقت ( {task_name} )\n"
            "—————————————\n"
            "🕒 أمامك 20 ثانية للحل!\n\n"
            f"💡 السؤال: {question}\n"
            "—————————————\n"
            "🚀 أسرع واحد يرسل الحل يفوز!"
        )
        bot.send_message(chat_id, msg)

    @bot.message_handler(func=lambda m: m.chat.id in active_time_challenges)
    def check_time_answer(m):
        chat_id = m.chat.id
        challenge = active_time_challenges[chat_id]
        
        # التحقق من الإجابة (مع تجاهل المسافات الزائدة في التفكيك)
        user_answer = m.text.strip()
        
        if user_answer == challenge["answer"]:
            elapsed = round(time.time() - challenge["start_time"], 2)
            
            if elapsed <= 20:
                bot.reply_to(m, f"✅ وحش الإمبراطورية!\n⚡ أجبت بشكل صحيح خلال {elapsed} ثانية.\n💰 تم إضافة 50 نقطة لرصيدك.")
            else:
                bot.reply_to(m, f"🐢 إجابة صحيحة ولكنك بطيء! استغرقت {elapsed} ثانية والحد المسموح 20.")
            
            del active_time_challenges[chat_id]
