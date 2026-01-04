from db_manager import get_user_gold, update_user_gold, add_item

COMMANDS = ["متجر", "شراء"]

ITEMS = [
    {"name": "سيف الإمبراطور", "price": 500, "desc": "زيادة ذهب عند الفوز بالنرد +20% ⚔️"},
    {"name": "درع الحصن", "price": 300, "desc": "تقلل الخسارة في النرد -50% 🛡️"},
    {"name": "جرعة شفاء", "price": 100, "desc": "تعيد 50 نقطة حياة 🧪"},
    {"name": "خوذة الحكيم", "price": 200, "desc": "زيادة الهدايا اليومية +50 ذهب 🧠"},
    {"name": "خاتم الحظ", "price": 400, "desc": "زيادة فرصة النرد للوصول 5 أو 6 +10% 🍀"},
    {"name": "سوار الذهب", "price": 350, "desc": "زيادة المكافآت من الألعاب المستقبلية +15% 💰"},
    {"name": "عباءة الظلال", "price": 600, "desc": "تقلل الخسارة في أي لعبة -20% 🌑"},
    {"name": "تميمة الحظ", "price": 250, "desc": "ربح عشوائي إضافي عند أخذ الهدايا 🎁"},
    {"name": "حجر الزمن", "price": 800, "desc": "يعطي فرصة لعب ثانية على النرد 🕰️"},
    {"name": "قفاز القوة", "price": 450, "desc": "زيادة الذهب من أي لعبة +25% 🧤"},
    {"name": "عصا الساحر", "price": 700, "desc": "مرة يومياً تحصل ربح عشوائي 🎇"},
    {"name": "خوذة التنين", "price": 1000, "desc": "فرصة نادرة جداً +300 ذهب على النرد 🐉"},
]

def handle(bot, message):
    text = message.text.strip()
    uid = message.from_user.id

    if text == "متجر":
        shop_text = "🛒 متجر الإمبراطورية:\n\n"
        for i, item in enumerate(ITEMS, start=1):
            shop_text += f"{i}. {item['name']} - {item['price']} ذهب\n   {item['desc']}\n"
        shop_text += "\nلشراء: اكتب 'شراء <رقم العنصر>'"
        bot.reply_to(message, shop_text)
        return

    if text.startswith("شراء"):
        parts = text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            bot.reply_to(message, "❌ استخدم: شراء <رقم العنصر>")
            return

        index = int(parts[1]) - 1
        if index < 0 or index >= len(ITEMS):
            bot.reply_to(message, "❌ رقم العنصر غير صالح")
            return

        item = ITEMS[index]
        gold = get_user_gold(uid)

        if gold < item["price"]:
            bot.reply_to(message, f"❌ رصيدك غير كافي لشراء {item['name']}")
            return

        update_user_gold(uid, -item["price"])
        add_item(uid, item["name"])
        bot.reply_to(message, f"✅ تم شراء {item['name']}!\n💰 رصيدك الحالي: {get_user_gold(uid)} ذهب")
