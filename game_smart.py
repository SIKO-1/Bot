import random
from telebot import types

# نظام النقاط المرتبط بالـ Volume
try:
    from db_manager import get_user, update_user
except:
    def get_user(uid): return {"balance": 0}
    def update_user(uid, k, v): pass

def register_handlers(bot):
    
    active_smart_challenges = {}

    # يستجيب للأوامر الملكية
    @bot.message_handler(func=lambda m: m.text in ['اذكى', 'ذكي', 'الاذكى'])
    def start_smart_game(m):
        chat_id = m.chat.id
        
        # قائمة رموز احترافية وصعبة (قوة ملاحظة عالية)
        emoji_sets = [
            ("🍎", "🍏"), ("🦁", "🐯"), ("🌑", "🌒"), 
            ("⌚️", "📱"), ("⚽️", "🏀"), ("💎", "💍"),
            ("🌋", "🔥"), ("🌲", "🌳"), ("👑", "🎩"),
            ("🏅", "🥇"), ("🐼", "🐻"), ("⛈", "🌩"),
            ("🧊", "❄️"), ("🍓", "🍒"), ("🕋", "🕌")
        ]
        
        # اختيار طقم رموز عشوائي
        main_emoji, diff_emoji = random.choice(emoji_sets)
        
        # إنشاء شبكة من 12 رمز (أصعب من القديمة)
        grid = [main_emoji] * 11
        grid.insert(random.randint(0, 11), diff_emoji)
        
        active_smart_challenges[chat_id] = {"answer": diff_emoji}

        # زخرفة إمبراطورية ملكية
        text = (
            "┏━━━━━━━ ● ━━━━━━━┓\n"
            "         ⌯ تـحـدي الأذ كـى ⌯\n"
            "┗━━━━━━━ ● ━━━━━━━┛\n\n"
            "  » استخرج الرمز المختلف من بين هذه الرموز :\n\n"
            f"          [ {''.join(grid)} ]\n\n"
            "⚠️ أرسل الإيموجي المختلف الآن\n"
            "💰 الـجـائـزة : 100 نـقـطـة"
        )
        bot.send_message(chat_id, text)

    @bot.message_handler(func=lambda m: m.chat.id in active_smart_challenges)
    def check_smart_answer(m):
        chat_id = m.chat.id
        correct = active_smart_challenges[chat_id]["answer"]
        
        # التحقق من الإجابة
        if m.text.strip() == correct:
            uid = m.from_user.id
            bal = get_user(uid).get("balance", 0)
            update_user(uid, "balance", bal + 100)
            
            # رسالة الفوز باللقب الملكي
            win_text = (
                "⌯ تـم الـتـحـقـق مـن الأذ كـى ⌯\n"
                "━━━━━━━━━━━━━━\n"
                f"👤 الـفـائـز : {m.from_user.first_name}\n"
                "🏆 الـلـقـب : الإمـبـراطـور الأذ كـى\n"
                "✅ الإجـابـة : صـحـيـحـة\n"
                "💰 الـجـوائـز : +100 نـقـطـة"
            )
            bot.reply_to(m, win_text)
            del active_smart_challenges[chat_id]
