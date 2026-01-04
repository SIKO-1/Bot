import random
import db_manager

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "نبض")
    def pulse_game(m):
        # الحارس الإمبراطوري (تجاهل المحظورين)
        if db_manager.get_user(m.from_user.id).get("banned"):
            return

        # قوائم المتعة (يمكنك زيادتها كما تشاء يا مولاي)
        psychological_states = [
            "مستقر وهادئ كالبحر", "متوتر قليلاً", "سعيد جداً", 
            "عاشق ولهان", "مرهق ويحتاج للنوم", "متحمس للمغامرة", 
            "في قمة الرواق", "مشتاق لأحدهم", "ممتن للحياة"
        ]

        advices = [
            "تحدث أقل، استمع أكثر.",
            "ابتسم، فجمال وجهك لا يليق به العبوس.",
            "لا تأخذ الأمور على محمل الشخصية دائماً.",
            "خذ نفساً عميقاً، كل شيء سيكون بخير.",
            "اعتزل ما يؤذيك، ولو كان غالياً.",
            "اجعل يومك مليئاً باللطف، وسيعود إليك.",
            "القليل من الهدوء يحل الكثير من العقد.",
            "بادر بالسلام، فكلمة طيبة تفتح مغاليق القلوب."
        ]

        # اختيار القيم عشوائياً
        pulse_rate = random.randint(60, 100)
        state = random.choice(psychological_states)
        advice = random.choice(advices)
        user_name = m.from_user.first_name

        # صياغة الرد
        response = (
            f" - نبض {user_name}: {pulse_rate}/100\n"
            f" - الحالة النفسية: {state}\n"
            f" - نصيحة للحياة: {advice}"
        )

        bot.reply_to(m, response)
