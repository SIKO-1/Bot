from db_manager import get_balance, update_balance, update_level

def register_shop_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text in ["متجر", "المتجر", "شوب", "shop"])
    def send_shop_list(m):
        shop_text = (
            "⌔︙قائمة متجر الإمبراطورية\n"
            "—————————————\n"
            "⌔︙شراء درع » 3000\n"
            "⌔︙شراء عفو » 5000\n"
            "⌔︙شراء هوية » 1000\n"
            "⌔︙شراء مضاعفة » 10,000\n"
            "⌔︙شراء صندوق الحظ » 1000\n"
            "⌔︙شراء الكنز » 1000\n"
            "⌔︙إرسال عيدية » 200\n"
            "⌔︙الرسالة المثبته » 100\n"
            "⌔︙شراء رفع مستوى » 500\n"
            "⌔︙تغيير بايو صديق » 1000\n"
            "—————————————\n"
            "💡 اكتب [ شراء + اسم الغرض ]"
        )
        bot.reply_to(m, shop_text)

    @bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
    def process_purchase(m):
        user_id = m.from_user.id
        command = m.text.replace("شراء ", "").strip()
        
        # قائمة الأسعار الرسمية
        prices = {
            "درع": 3000, "عفو": 5000, "هوية": 1000, 
            "مضاعفة": 10000, "صندوق الحظ": 1000, "الكنز": 1000, 
            "عيدية": 200, "رسالة مثبتة": 100, "بايو صديق": 1000
        }

        money = get_balance(user_id)

        # 🆙 معالجة رفع المستوى
        if command.startswith("رفع مستوى"):
            try:
                parts = command.split()
                lvl = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 10
                cost = (lvl // 10) * 500
                if cost < 500: cost = 500

                if money >= cost:
                    update_balance(user_id, -cost)
                    update_level(user_id, lvl)
                    bot.reply_to(m, f"🆙 تمت الترقية بمقدار {lvl} مستويات!\n💸 الخصم: {cost} ذهبة.")
                else:
                    bot.reply_to(m, f"❌ رصيدك ({money}) لا يكفي لهذه الترقية.")
            except:
                bot.reply_to(m, "⚠️ استخدم: شراء رفع مستوى 10")
            return

        # 🛍️ المشتريات العادية
        if command in prices:
            price = prices[command]
            if money >= price:
                update_balance(user_id, -price)
                bot.reply_to(m, f"✅ تم شراء {command} بنجاح!\n💰 المتبقي: {money - price}")
            else:
                bot.reply_to(m, f"❌ رصيدك ({money}) لا يكفي لشراء {command}.")
