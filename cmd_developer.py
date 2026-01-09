def handle(bot, message):
    if not message.text:
        return

    if message.text.strip() != "المطور":
        return

    DEV_ID = 5860391324  # آيدي المطور

    # اقتباس فلسفي مجنون
    quote = (
        "↫ اقتباس عن المطور:\n"
        "⌁ *\"المطور لا يكتب أوامر…*\n"
        "*هو يخلق قوانين، ثم يراقب الفوضى وهي تطيع.\"*"
    )

    try:
        chat = bot.get_chat(DEV_ID)

        user_id = chat.id
        username = f"@{chat.username}" if chat.username else "لا يوجد"
        name = chat.first_name or "المطور"
        bio = chat.bio if chat.bio else "لا يوجد"

        # محاولة جلب الرتبة من ملف الرتب
        try:
            import db_manager
            rank = db_manager.get_rank(user_id)
            if not rank:
                rank = "المطور الأعلى 👑"
        except:
            rank = "المطور الأعلى 👑"

        text = (
            f"{quote}\n\n"
            "⌁︙ايدي الـمُطَور↫ `{}`\n"
            "⌁︙معرف الـمُطَور↫ {}\n"
            "⌁︙حساب الـمُطَور↫ المطور الأساسي\n"
            "⌁︙رتبة الـمُطَور↫ {}\n"
            "⌁︙البـايـــو↫ {}"
        ).format(user_id, username, rank, bio)

        # جلب صورة الحساب
        photos = bot.get_user_profile_photos(DEV_ID, limit=1)

        if photos.total_count > 0:
            photo_id = photos.photos[0][-1].file_id
            bot.send_photo(
                message.chat.id,
                photo_id,
                caption=text,
                parse_mode="Markdown"
            )
        else:
            bot.send_message(
                message.chat.id,
                text,
                parse_mode="Markdown"
            )

    except Exception:
        bot.send_message(
            message.chat.id,
            "⚠️ تعذّر جلب معلومات المطور حالياً."
        )
