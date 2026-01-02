import random
from db_manager import get_user

def register_handlers(bot):
    # الآيدي الخاص بك كإمبراطور (السيادة المطلقة)
    DEV_ID = 5860391324

    # قائمة الجمل العراقية الملكية (15 جملة بين الغزل والهيبة والمزاح)
    IRAQI_QUOTES = [
        "يـا بـعـد الـروح والـجـبـد والـرية",
        "وجهـك حـلـو مـثـل صـمـون عـراقـي حـار",
        "أحـبـك حـب الـعـراقي لـلـچـاي الـمـهـيـل",
        "انـت مـثـل الـتـبـسي.. مـحـد يـشـبـع مـنـك",
        "يـا نـبـع الـريـحـان بـنـص بـغـداد",
        "وجـهـك يـطـرد الـفـكـر ويـجـيـب الـخـيـر",
        "لـو كـل الـبـشـر مـثـلـك چـان الـدنـيـا بـخـيـر",
        "ضـحـكـتـك تـرد الـعـافـيـة لـلـگـلـب",
        "يـا أول بـشـر يـمـشـي بـنـص شـرايـيـنـي",
        "كـلـك ذوق مـن الـجـدم لـلـهـامـة",
        "انـت الـسـنـد والـظـهـر بـوكـت الـضـيـك",
        "يـا مـن جـمـالـك مـثـل غـروب دجـلـة",
        "أريـدك ويـاي لـحـد مـا يـطـلـع نـخـل بـراسـي",
        "عـيـونـك بـيـهـا لـمـعـة مـثـل دجـلـة والـفـرات",
        "يـا بـعـد شـيـبـي وشـبـابـي والـنـبـض مـالـتـي"
    ]

    # --- قسم ديوان الأوامر ---
    @bot.message_handler(func=lambda message: message.text in ["اوامر", "الأوامر", "الاوامر", "قائمة"])
    def luxury_menu(message):
        name = message.from_user.first_name
        user_id = message.from_user.id
        
        menu_text = (
            "╔═════════════════╗\n"
            "   الاوامر الإمبراطورية \n"
            "╚═════════════════╝\n\n"
            f"مرحباً بك في حضرة العرش\n"
            f"السيد : **{name}**\n"
            "━━━━━━━━━━━━━━━\n\n"
            "مراسيم وأقسام الامبراطورية :\n"
            "┌──────────────┐\n"
            "   --  الألعاب\n"
            "   --  المتجر\n"
            "   -- مستوى\n"
            "   -- الإمبراطورية \n"
            "└──────────────┘\n"
        )

        # يظهر فقط لك كإمبراطور
        if user_id == DEV_ID:
            menu_text += (
                "\nشؤون القصر العالي\n"
                "   -- الإمـبـراطـوريـة\n"
                "( صلاحيات السيادة المطلقة )\n"
                "━━━━━━━━━━━━━━━\n"
            )
        
        menu_text += (
            "لعرض هويتك أرسل  [ ا ]\n"
            "━━━━━━━━━━━━━━━\n"
            "تخضع الرعايا لهيبتك"
        )
        bot.reply_to(message, menu_text, parse_mode="Markdown")

    # --- قسم الهوية الإمبراطورية (الايدي) ---
    @bot.message_handler(func=lambda message: message.text in ["ايدي", "ا", "ID"])
    def luxury_id(message):
        uid = message.from_user.id
        name = message.from_user.first_name
        username = message.from_user.username if message.from_user.username else "لا يوجد"
        user_data = get_user(uid)
        
        balance = user_data.get("balance", 0)
        rank = user_data.get("rank", "مواطن")
        
        # جلب البايو الفعلي من حساب المستخدم
        try:
            full_user = bot.get_chat(uid)
            bio = full_user.bio if full_user.bio else "خالي من الكلمات"
        except:
            bio = "غير متاح حالياً"

        # نظام التفاعل الساخر
        # ملاحظة: يجب أن يكون لديك حقل 'messages' في قاعدة البيانات لتتبع التفاعل
        messages_count = user_data.get("messages", 0) 
        if messages_count > 500:
            activity = "متفاعل نار وشعلة"
        else:
            activity = "نايم بالعسل.. تحرك شوية لا تخليني أطردك"

        # فحص تميز الحساب (قصر الآيدي دليل قدم الحساب)
        account_type = "حساب ملكي مميز" if uid < 1000000000 else "حساب برعية بسيطة"

        # اختيار جملة عراقية عشوائية
        quote = random.choice(IRAQI_QUOTES)

        id_card = (
            f"↫ {quote}\n"
            "━━━━━━━━━━━━━━━\n"
            f"⌁︙ايديـڪ↫ `{uid}`\n"
            f"⌁︙معرفـڪ↫ @{username}\n"
            f"⌁︙حسابـڪ↫ {account_type}\n"
            f"⌁︙تفاعلـڪ↫ {activity}\n"
            f"⌁︙رصيـدڪ↫ {balance}\n"
            f"⌁︙البـايـــو↫ {bio}\n"
            "━━━━━━━━━━━━━━━\n"
            f"الرتبة السيادية : {rank}"
        )

        try:
            photos = bot.get_user_profile_photos(uid)
            if photos.total_count > 0:
                bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=id_card, parse_mode="Markdown")
            else:
                bot.reply_to(message, id_card, parse_mode="Markdown")
        except:
            bot.reply_to(message, id_card, parse_mode="Markdown")
