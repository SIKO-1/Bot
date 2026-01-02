import random
import db_manager

def register_handlers(bot): # تأكد أن الاسم register_handlers ليتعرف عليه الـ main
    
    RANKS = {
        "مبتدئ": 0, "مكافح": 50, "صياد": 150, "جندي": 300, "فارس": 500,
        "مغوار": 800, "قناص": 1200, "زعيم": 2000, "شيخ": 3500, "باشا": 5000,
        "سفير": 7000, "وزير": 10000, "حاكم": 15000, "سلطان": 20000, "ملك": 30000,
        "دوق": 45000, "بارون": 60000, "كونت": 80000, "ماركيز": 100000, "أمير": 150000,
        "ولي عهد": 200000, "جنرال": 300000, "مشير": 500000, "أسطورة": 1000000, "إمبراطور": 9999999
    }

    # 1. أمر مستوى (أولوية عالية)
    @bot.message_handler(func=lambda m: m.text in ["مستوى", "مستواي"])
    def show_level(m):
        uid = str(m.from_user.id)
        user = db_manager.get_user(uid)
        lvl = user.get('level', 1)
        xp = user.get('xp', 0)
        rank = db_manager.get_rank(uid)
        diff = (lvl // 50) + 1
        needed = lvl * (10 * diff)
        
        txt = (
            "📊 **الـسـجـل الإمـبـراطـوري**\n"
            "————————————————\n"
            f"👑 الـرتبـة: **[{rank}]**\n"
            f"⭐ الـمـسـتـوى: {lvl}\n"
            f"💠 الـخـبـرة: {xp}/{needed}\n"
            "————————————————"
        )
        bot.reply_to(m, txt, parse_mode="Markdown")

    # 2. أمر رتب ورتبتي
    @bot.message_handler(func=lambda m: m.text in ["رتب", "الرتب"])
    def show_ranks(m):
        txt = "📜 **الـمـراتـب والأسـعـار:**\n"
        for n, p in list(RANKS.items())[:10]: # عرض أول 10 كمثال للسكرين
            txt += f"🔹 {n} » {p}\n"
        txt += "... (اكتب شراء رتبة + الاسم)"
        bot.reply_to(m, txt)

    @bot.message_handler(func=lambda m: m.text == "رتبتي")
    def my_rank(m):
        rank = db_manager.get_rank(m.from_user.id)
        bot.reply_to(m, f"🛡️ رتبتك: **[{rank}]**")

    # 3. نظام الخبرة التلقائي (يوضع في الآخر لكي لا يعطل الأوامر)
    @bot.message_handler(func=lambda m: True)
    def handle_xp(m):
        # التحقق أن الرسالة ليست أمراً لبوت آخر أو لهذا البوت
        if m.text and not m.text.startswith("/"):
            leveled_up, new_lvl = db_manager.update_xp(m.from_user.id, 5)
            if leveled_up:
                gift = random.randint(1, 500)
                db_manager.update_balance(m.from_user.id, gift)
                bot.reply_to(m, f"🆙 **تـرقـيـة!** لفل **{new_lvl}**\n🎁 المكافأة: **{gift}** ذهبة")
