import db_manager

# ======================
# تعريف الرتب
# ======================
RANKS = [
    {"level": 1, "name": "المبتدئ", "price": 100*5},
    {"level": 2, "name": "المستكشف", "price": 200*5},
    {"level": 3, "name": "المقاتل", "price": 300*5},
    {"level": 4, "name": "الحارس", "price": 400*5},
    {"level": 5, "name": "الفارس", "price": 500*5},
    {"level": 6, "name": "الأسطوري", "price": 600*5},
    {"level": 7, "name": "البطل", "price": 700*5},
    {"level": 8, "name": "المنقذ", "price": 800*5},
    {"level": 9, "name": "القائد", "price": 900*5},
    {"level": 10, "name": "الجنرال", "price": 1000*5},
    {"level": 11, "name": "الفاتح", "price": 1100*5},
    {"level": 12, "name": "الزعيم", "price": 1200*5},
    {"level": 13, "name": "المنتصر", "price": 1300*5},
    {"level": 14, "name": "المهيمن", "price": 1400*5},
    {"level": 15, "name": "القيصر", "price": 1500*5},
    {"level": 16, "name": "الملك", "price": 1600*5},
    {"level": 17, "name": "الإمبراطور", "price": 1700*5},  # فقط هذا يستطيع ترقية الآخرين
    {"level": 18, "name": "الناصر", "price": 1800*5},
    {"level": 19, "name": "العظيم", "price": 1900*5},
    {"level": 20, "name": "السامي", "price": 2000*5},
    {"level": 21, "name": "الراقي", "price": 2100*5},
    {"level": 22, "name": "المرموق", "price": 2200*5},
    {"level": 23, "name": "الخارق", "price": 2300*5},
    {"level": 24, "name": "الأسطورة", "price": 2400*5},
    {"level": 25, "name": "الإمبراطور الأعلى", "price": 0},  # لا يمكن شراءها
]

SPECIAL_DEV_RANK = {"level": 100, "name": "المطور", "price": 0}

# ======================
# دوال مساعدة
# ======================
def get_rank(uid):
    user = db_manager._get_user(uid)
    return user.get("rank_level", 1)

def set_rank(uid, level):
    db_manager.users.update_one({"uid": uid}, {"$set": {"rank_level": level}})

def get_rank_info(level):
    if level == SPECIAL_DEV_RANK["level"]:
        return SPECIAL_DEV_RANK
    for r in RANKS:
        if r["level"] == level:
            return r
    return RANKS[0]

def can_buy_rank(uid, target_level):
    current_level = get_rank(uid)
    if target_level <= current_level:
        return False, "🚫 لا يمكنك ترقية إلى رتبة أقل أو مساوية لرتبتك الحالية."
    if target_level > current_level + 1:
        return False, "🚫 يجب شراء الرتب خطوة خطوة."
    rank = get_rank_info(target_level)
    if rank["price"] == 0:
        return False, "🚫 لا يمكن شراء هذه الرتبة، يجب أن يتم ترقيتها من قبل الإمبراطور."
    user_gold = db_manager.get_user_gold(uid)
    if user_gold < rank["price"]:
        return False, f"🚫 لا تملك ذهب كافي، سعر الرتبة {rank['price']} ذهب"
    return True, ""

def buy_rank(uid, target_level):
    ok, msg = can_buy_rank(uid, target_level)
    if not ok:
        return False, msg
    rank = get_rank_info(target_level)
    db_manager.update_user_gold(uid, -rank["price"])
    set_rank(uid, target_level)
    return True, f"✅ تم ترقيتك إلى رتبة {rank['name']}"

def upgrade_by_emperor(emperor_uid, target_uid, target_level):
    if get_rank(emperor_uid) != 17:  # رتبة الإمبراطور
        return False, "🚫 فقط الإمبراطور يمكنه استخدام أمر الترقية"
    rank = get_rank_info(target_level)
    set_rank(target_uid, target_level)
    return True, f"✅ تم ترقية المستخدم إلى رتبة {rank['name']} بواسطة الإمبراطور"

# ======================
# موديول البوت
# ======================
COMMANDS = ["رتب", "رتبتي"]

def handle(bot, message):
    text = message.text.strip()
    uid = message.from_user.id

    # عرض قائمة الرتب
    if text == "رتب":
        lines = ["🏆 قائمة الرتب:"]
        for r in RANKS:
            price_text = f"{r['price']} ذهب" if r['price'] > 0 else "— لا يمكن الشراء —"
            lines.append(f"{r['level']}- {r['name']} : {price_text}")
        bot.reply_to(message, "\n".join(lines))
        return

    # عرض رتبة المستخدم
    if text == "رتبتي":
        level = get_rank(uid)
        rank = get_rank_info(level)
        bot.reply_to(message, f"🎖 رتبتك الحالية: {rank['name']} (مستوى {rank['level']})")
        return

    # شراء رتبة خطوة بخطوة
    if text.startswith("رتبة "):
        try:
            target_level = int(text.split()[1])
        except:
            bot.reply_to(message, "🚫 الرجاء إدخال رقم رتبة صالح")
            return
        success, msg = buy_rank(uid, target_level)
        bot.reply_to(message, msg)
        return

    # ترقية الإمبراطور
    if text.startswith("ترقية "):
        parts = text.split()
        if len(parts) < 3:
            bot.reply_to(message, "💡 مثال: ترقية @username 5 أو ترقية 123456789 5")
            return
        target = parts[1]
        try:
            target_level = int(parts[2])
        except:
            bot.reply_to(message, "🚫 رقم الرتبة غير صالح")
            return

        # تحويل اسم المستخدم إلى UID إذا كان باليوزرنيم
        try:
            target_uid = int(target)
        except:
            user = db_manager.users.find_one({"username": target.lstrip("@")})
            if not user:
                bot.reply_to(message, "🚫 لم أتمكن من إيجاد المستخدم")
                return
            target_uid = user["uid"]

        success, msg = upgrade_by_emperor(uid, target_uid, target_level)
        bot.reply_to(message, msg)
