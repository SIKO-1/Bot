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
        user_id = str(m.from_user.id)
        command = m.text.replace("شراء ", "").strip()
        
        # قائمة الأسعار [cite: 2026-01-02]
        prices = {
            "درع": 3000, "عفو": 5000, "هوية": 1000, 
            "مضاعفة": 10000, "صندوق الحظ": 1000, "الكنز": 1000, 
            "عيدية": 200, "رسالة مثبتة": 100, "بايو صديق": 1000
        }

        # التأكد من وجود الدوال في db_manager لتجنب الانهيار
        if hasattr(db_manager, 'get_balance'):
            money = db_manager.get_balance(user_id)
        else:
            # حل بديل إذا فشل الجسر
            user_data = db_manager.get_user(user_id)
            money = user_data.get('balance', 0)

        if command in prices:
            price = prices[command]
            if money >= price:
                # استخدام دالة التحديث التي أضفتها
                if hasattr(db_manager, 'update_balance'):
                    db_manager.update_balance(user_id, -price)
                else:
                    db_manager.update_user(user_id, 'balance', money - price)
                
                bot.reply_to(m, f"✅ تم شراء {command} بنجاح!\n💰 رصيدك المتبقي: {money - price}")
            else:
                bot.reply_to(m, f"❌ رصيدك ({money}) لا يكفي لشراء {command}.")
