def handle(bot, message):
    if not message.text:
        return

    if message.text.strip() != "المطور":
        return

    DEV_ID = 5860391324  # آيدي المطور

    # اقتباس فلسفي مجنون
    quote = (
        "↫ اقتباس عن المطور:\n"
        "⌁︙\"المطور لا يكتب أوامر…\n"
        "هو يخلق قوانين، ثم يراقب الفوضى وهي تطيع.\""
    )

    # بيانات ثابتة وآمنة
    user_id = DEV_ID
    username = "@Om_rtl"  # ← حط معرفك هنا
    rank = "المطور الأعلى 👑"
    bio = "لا يوجد"

    # محاولة جلب الرتبة من db
    try:
        import db_manager
        db_rank = db_manager.get_rank(user_id)
        if db_rank:
            rank = db_rank
    except:
        pass

    text = (
        f"{quote}\n\n"
        f"⌁︙ايدي الـمُطَور↫ {user_id}\n"
        f"⌁︙معرف الـمُطَور↫ {username}\n"
        f"⌁︙حساب الـمُطَور↫ المطور الأساسي\n"
        f"⌁︙رتبة الـمُطَور↫ {rank}\n"
        f"⌁︙البـايـــو↫ {bio}"
    )

    # محاولة جلب صورة الحساب
    try:
        photos = bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            photo_id = photos.photos[0][-1].file_id
            bot.send_photo(message.chat.id, photo_id, caption=text)
            return
    except:
        pass

    # إذا ماكو صورة
    bot.send_message(message.chat.id, text)
