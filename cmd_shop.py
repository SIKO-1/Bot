import db_manager

def register_shop_handlers(bot):
    
    # دالة ذكية لإيجاد دالة الرصيد والخصم مهما كان اسمها في ملفك
    def call_db_func(user_id, amount=None, mode="get"):
        # قائمة الأسماء المحتملة التي قد تكون استخدمتها في db_manager
        get_names = ['get_balance', 'get_money', 'get_points', 'get_user_balance', 'get_user_points']
        update_names = ['update_balance', 'update_money', 'update_points', 'update_user_balance', 'update_user_points']
        
        target_list = get_names if mode == "get" else update_names
        
        for func_name in target_list:
            if hasattr(db_manager, func_name):
                func = getattr(db_manager, func_name)
                return func(user_id) if mode == "get" else func(user_id, amount)
        return 0

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
            "⌔︙رفع المستوى » 500\n"
            "⌔︙بايو صديق » 1000\n"
            "⌔︙الرتب » لعرض الرتب\n"
            "—————————————\n"
            "💡 اكتب [ شراء + اسم الغرض ]"
        )
        bot.reply_to(m, shop_text)

    @bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
    def process_purchase(m):
        user_id = m.from_user.id
        command = m.text.replace("شراء ", "").strip()
        
        # الأسعار التي حددتها أنت [cite: 2026-01-02]
        prices = {
            "درع": 3000, "عفو": 5000, "هوية": 1000, 
            "مضاعفة": 10000, "صندوق الحظ": 1000, "الكنز": 1000, 
            "عيدية": 200, "رسالة مثبتة": 100, "بايو صديق": 1000
        }

        current_money = call_db_func(user_id, mode="get")

        if command.startswith("رفع مستوى"):
            try:
                parts = command.split()
                lvl_to_add = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 10
                cost = (lvl_to_add // 10) * 500
                if cost < 500: cost = 500

                if current_money >= cost:
                    call_db_func(user_id, -cost, mode="update")
                    if hasattr(db_manager, 'update_level'):
                        db_manager.update_level(user_id, lvl_to_add)
                    bot.reply_to(m, f"🆙 تم رفع مستواك بمقدار {lvl_to_add}.\n💸 الخصم: {cost} ذهبة.")
                else:
                    bot.reply_to(m, f"❌ رصيدك ({current_money}) لا يكفي!")
            except:
                bot.reply_to(m, "⚠️ استخدم: شراء رفع مستوى 10")
            return

        if command in prices:
            price = prices[command]
            if current_money >= price:
                call_db_func(user_id, -price, mode="update")
                bot.reply_to(m, f"✅ تم شراء {command} بنجاح!\n💰 المتبقي: {current_money - price}")
            else:
                bot.reply_to(m, f"❌ رصيدك {current_money} لا يكفي.")
