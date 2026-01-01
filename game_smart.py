import random

def register_handlers(bot):
    
    active_smart_challenges = {}

    # يستجيب لـ (اذكى، ذكي، الاذكى)
    @bot.message_handler(func=lambda m: m.text in ['اذكى', 'ذكي', 'الاذكى'])
    def start_smart_game(m):
        chat_id = m.chat.id
        
        # قائمة الرموز المستخدمة في التحدي
        emoji_sets = [
            ("🍎", "🍏"), ("🍋", "🍊"), ("🎈", "🏮"), 
            ("🐱", "🐶"), ("⚽", "🏀"), ("💎", "💍"),
            ("⭐", "🌟"), ("🌙", "🌤️"), ("🔥", "💥")
        ]
        
        # اختيار طقم رموز عشوائي
        main_emoji, diff_emoji = random.choice(emoji_sets)
        
        # إنشاء الشبكة (9 رموز متشابهة وواحد مختلف)
        grid = [main_emoji] * 9
        grid.insert(random.randint(0, 9), diff_emoji)
        
        active_smart_challenges[chat_id] = {"answer": diff_emoji}

        msg = (
            "⌔︙تحدي الأذكى ( قوة ملاحظة ) 🧠\n"
            "—————————————\n"
            "💡 أرسل الإيموجي المختلف من بين هذه الرموز:\n\n"
            f"📥 » {''.join(grid)}\n"
            "—————————————\n"
            "🚀 من هو أذكى إمبراطور سيجده أولاً؟"
        )
        bot.send_message(chat_id, msg)

    @bot.message_handler(func=lambda m: m.chat.id in active_smart_challenges)
    def check_smart_answer(m):
        chat_id = m.chat.id
        correct = active_smart_challenges[chat_id]["answer"]
        
        # التحقق إذا كان النص المرسل هو الإيموجي المختلف
        if m.text.strip() == correct:
            bot.reply_to(m, f"👑 كفو! لقب (الأذكى) لهذا الدور من نصيب: {m.from_user.first_name}\n💰 تم إضافة 100 نقطة لرصيدك.")
            del active_smart_challenges[chat_id]
