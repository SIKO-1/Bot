import db_manager

COMMANDS_USE = ["استخدم", "استعمل"]

ITEM_EFFECTS = {
    "سيف الإمبراطور 🔱": lambda uid: db_manager.update_user_gold(uid, 50),
    "درع الحماية الأسطوري 🛡️": lambda uid: db_manager.extend_protection(uid, 24*3600),
    "خاتم التفاعل 💍": lambda uid: db_manager.add_fake_messages(uid, 10),
    "عملة الإمبراطور 💰": lambda uid: db_manager.update_user_gold(uid, 1000),
    "كتاب الحكمة 📜": lambda uid: db_manager.add_random_rare_item(uid),
    "خوذة الحكيم 🪖": lambda uid: db_manager.reduce_gift_cooldown(uid, 0.5),
    "بلورة الزمن ⏳": lambda uid: db_manager.reset_daily_task(uid)
}

def handle(bot, message):
    uid = message.from_user.id
    text = message.text.strip()

    if any(text.startswith(cmd) for cmd in COMMANDS_USE):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "❌ اكتب اسم العنصر الذي تريد استخدامه بعد الأمر")
            return

        item_name = parts[1].strip()
        inventory = db_manager.get_inventory(uid)

        if item_name not in inventory:
            bot.reply_to(message, f"❌ لا يمكنك استخدام هذا العنصر لأنك لا تمتلكه في المخزون.")
            return

        # تنفيذ التأثير
        effect_func = ITEM_EFFECTS.get(item_name)
        if effect_func:
            effect_func(uid)
            db_manager.remove_from_inventory(uid, item_name)
            bot.reply_to(message, f"✅ استخدمت {item_name} وتم تطبيق تأثيره!")
        else:
            bot.reply_to(message, "❌ هذا العنصر ليس لديه تأثير محدد.")
