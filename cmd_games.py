import random
from db_manager import get_user, update_user

def register_handlers(bot):
    
    # --- 1. قائمة الألعاب (المنيو) ---
    @bot.message_handler(func=lambda m: m.text == "العاب")
    def games_menu(m):
        menu = (
            "🎮 **مركز الألعاب الإمبراطوري** 🎮\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            "🎲 **ألعاب الحظ والسرعة:**\n"
            "├ `نرد` - (تحدي الزهر الملكي)\n"
            "└ `تخمين` - (خمن الرقم من 1 لـ 10)\n\n"
            "🧠 **ألعاب الذكاء:**\n"
            "├ `سؤال` - (أسئلة عامة وجوائز)\n"
            "└ `رياضيات` - (تحدي الحساب)\n\n"
            "👑 **أباطرة (مقفل 🔐):**\n"
            "└ `الكنز` - (تحتاج رتبة إمبراطور)\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
        )
        bot.reply_to(m, menu, parse_mode="Markdown")

    # --- 2. لعبة النرد (تعمل فوراً) ---
    @bot.message_handler(func=lambda m: m.text == "نرد")
    def dice_game(m):
        dice_msg = bot.send_dice(m.chat.id)
        value = dice_msg.dice.value
        if value >= 4:
            update_user(m.from_user.id, "balance", get_user(m.from_user.id)["balance"] + 50)
            bot.reply_to(m, f"🎲 النتيجة {value}! مبروك ربحت 50 نقطة.")
        else:
            bot.reply_to(m, f"🎲 النتيجة {value}.. حظاً أوفر المرة القادمة.")

    # --- 3. لعبة الأسئلة (نظام الخطوة التالية) ---
    @bot.message_handler(func=lambda m: m.text == "سؤال")
    def quiz_game(m):
        questions = {
            "ما هي عاصمة العراق؟": "بغداد",
            "كم عدد ألوان قوس قزح؟": "7",
            "ما هو أكبر كوكب؟": "المشتري"
        }
        q, a = random.choice(list(questions.items()))
        msg = bot.reply_to(m, f"❓ **سؤال لك:** {q}\n\n_(أرسل الإجابة الآن)_")
        # هنا نخبر البوت أن ينتظر الرسالة القادمة من المستخدم ليمررها للدالة check_answer
        bot.register_next_step_handler(msg, lambda message: check_answer(message, a, bot))

    def check_answer(m, correct_answer, bot):
        uid = m.from_user.id
        if m.text.strip() == correct_answer:
            new_bal = get_user(uid)["balance"] + 100
            update_user(uid, "balance", new_bal)
            bot.reply_to(m, f"✅ إجابة صحيحة! مبروك حصلت على 100 نقطة.\n💰 رصيدك الحالي: {new_bal}")
        else:
            bot.reply_to(m, f"❌ خطأ! الإجابة هي: {correct_answer}")

    # --- 4. الألعاب المقفولة ---
    @bot.message_handler(func=lambda m: m.text == "الكنز")
    def treasure_game(m):
        user = get_user(m.from_user.id)
        if user.get("rank") != "إمبراطور":
            bot.reply_to(m, "⚠️ **عذراً!** هذه اللعبة للأباطرة فقط. اذهب للمتجر واشترِ الرتبة!")
        else:
            bot.reply_to(m, "🏰 أهلاً بك يا ملك! بدأت رحلة البحث عن الكنز...")
