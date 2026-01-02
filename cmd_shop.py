import db_manager

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
            "⌔︙صندوق الحظ » 1000\n"
            "⌔︙الكنز » 1000\n"
            "⌔︙إرسال عيدية » 200\n"
            "⌔︙الرسالة المثبته » 100\n"
            "⌔︙شراء رفع مستوى » 500\n"
            "⌔︙بايو صديق » 1000\n"
            "⌔︙الرتب » اكتب (الرتب) لعرضها\n"
            "—————————————\n"
            "💡 اكتب [ شراء + اسم الغرض ]"
        )
        bot.reply_to(m, shop_text)

    @bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
    def process_purchase(m):
        user_id = str(m.from_user.id)
        command = m.text.replace("شراء ", "").strip()
        
        prices = {
            "درع": 3000, "عفو": 5000, "هوية": 1000, 
            "مضاعفة": 10000, "صندوق الحظ": 1000, "الكنز": 1000, 
            "عيدية": 200, "رسالة مثبتة": 100, "بايو صديق": 1000
        }

        # جلب بيانات المستخدم من ملفك (نظام JSON)
        user_data = db_manager.get_user(user_id)
        current_balance = user_data.get('balance', 0)
        current_level = user_data.get('level', 1)

        # 🆙 حالة رفع المستوى (كل 10 بـ 500)
        if command.startswith("رفع مستوى"):
            try:
                parts = command.split()
                lvl_to_add = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 10
                cost = (lvl_to_add // 10) * 500
                if cost < 500: cost = 500

                if current_balance >= cost:
                    db_manager.update_user(user_id, 'balance', current_balance - cost)
                    db_manager.update_user(user_id, 'level', current_level + lvl_to_add)
                    bot.reply_to(m, f"🆙 هنيئاً! تم رفع مستواك بمقدار {lvl_to_add}.\n💸 تم خصم {cost} من رصيدك.")
                else:
                    bot.reply_to(m, f"❌ رصيدك ({current_balance}) لا يكفي!")
            except:
                bot.reply_to(m, "⚠️ استخدم: شراء رفع مستوى 10")
            return

        # 🛍️ المشتريات العادية
        if command in prices:
            price = prices[command]
            if current_balance >= price:
                db_manager.update_user(user_id, 'balance', current_balance - price)
                bot.reply_to(m, f"✅ تم شراء {command} بنجاح!\n💰 المتبقي: {current_balance - price}")
            else:
                bot.reply_to(m, f"❌ رصيدك ({current_balance}) لا يكفي لشراء {command}.")
