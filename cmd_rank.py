import db_manager

DEV_ID = 5860391324  # ايدي المطور
MAX_RANK = 25

RANKS = {
    0: ("بدون رتبة", 0),
    1: ("جندي", 500),
    2: ("محارب", 1200),
    3: ("فارس", 2500),
    4: ("قائد", 5000),
    5: ("نخبة", 9000),
    6: ("كابتن", 15000),
    7: ("جنرال", 22000),
    8: ("مارشال", 30000),
    9: ("بارون", 40000),
    10: ("كونت", 55000),
    11: ("دوق", 75000),
    12: ("أمير", 100000),
    13: ("ولي العهد", 140000),
    14: ("لورد", 190000),
    15: ("لورد أعلى", 250000),
    16: ("نبيل الإمبراطورية", 320000),
    17: ("حاكم", 400000),
    18: ("حاكم أعلى", 500000),
    19: ("ملك", 650000),
    20: ("ملك عظيم", 850000),
    21: ("إمبراطور صغير", 1100000),
    22: ("إمبراطور", 1500000),
    23: ("إمبراطور أعظم", 2000000),
    24: ("ظل الإمبراطور", 3000000),
    25: ("👑 الإمبراطور المطلق 👑", None),  # لا تُشترى
}

def handle(bot, message):
    text = message.text.strip()
    uid = message.from_user.id

    # ======================
    # عرض الرتب
    # ======================
    if text == "رتب":
        msg = "🏷️ قائمة الرتب:\n\n"
        for i in range(1, MAX_RANK + 1):
            name, price = RANKS[i]
            if price is None:
                msg += f"{i}. {name} — ❌ خاصة\n"
            else:
                msg += f"{i}. {name} — 💰 {price}\n"
        bot.reply_to(message, msg)
        return

    # ======================
    # رتبتي
    # ======================
    if text == "رتبتي":
        rank = db_manager.get_user_rank(uid)
        name, _ = RANKS.get(rank)
        bot.reply_to(message, f"🎖️ رتبتك الحالية:\n{name} (#{rank})")
        return

    # ======================
    # شراء رتبة
    # ======================
    if text.startswith("رتبة"):
        try:
            target = int(text.split()[1])
        except:
            bot.reply_to(message, "❌ اكتب: رتبة رقم")
            return

        current = db_manager.get_user_rank(uid)

        if target != current + 1:
            bot.reply_to(message, "❌ لازم تشتري الرتب بالترتيب")
            return

        name, price = RANKS.get(target, (None, None))

        if price is None:
            bot.reply_to(message, "🚫 هذه الرتبة لا تُشترى")
            return

        gold = db_manager.get_user_gold(uid)
        if gold < price:
            bot.reply_to(message, "💸 ذهبك غير كافي")
            return

        db_manager.update_user_gold(uid, -price)
        db_manager.set_user_rank(uid, target)

        bot.reply_to(
            message,
            f"✅ تمت الترقية!\n🎖️ رتبتك الجديدة: {name}"
        )
        return

    # ======================
    # ترقية (للمطور فقط)
    # ======================
    if text.startswith("ترقية"):
        if uid != DEV_ID:
            return

        parts = text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ الصيغة: ترقية ايدي الرتبة")
            return

        try:
            target_uid = int(parts[1])
            target_rank = int(parts[2])
        except:
            bot.reply_to(message, "❌ ايدي أو رتبة غير صحيحة")
            return

        if target_rank not in RANKS:
            bot.reply_to(message, "❌ رتبة غير موجودة")
            return

        db_manager.set_user_rank(target_uid, target_rank)
        name, _ = RANKS[target_rank]

        bot.reply_to(
            message,
            f"👑 تمت الترقية بالقوة الإمبراطورية!\n"
            f"الرتبة الجديدة: {name}"
        )
