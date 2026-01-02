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
            "⌔︙رفع المستوى » 500\n"
            "⌔︙بايو صديق » 1000\n"
            "⌔︙الرتب » لعرض الرتب المتاحة\n"
            "—————————————\n"
            "💡 اكتب [ شراء + اسم الغرض ]"
        )
        bot.reply_to(m, shop_text)

    @bot.message_handler(func=lambda m: m.text and m.text.startswith("شراء "))
    def process_purchase(m):
        user_id = m.from_user.id
        command = m.text.replace("شراء ", "").strip()
        
        prices = {
            "درع": 3000, "عفو": 5000, "هوية": 1000, 
            "مضاعفة": 10000, "صندوق الحظ": 1000, "الكنز": 1000, 
            "عيدية": 200, "رسالة مثبتة": 100, "بايو صديق": 1000
        }

        # محاولة جلب الرصيد بأسماء دوال بديلة لتجنب الخطأ
        try:
            current_money = db_manager.get_money(user_id)
        except AttributeError:
            try:
                current_money = db_manager.get_coins(user_id)
            except AttributeError:
                bot.reply_to(m, "⚠️ خطأ فني: لم أستطع العثور على محفظتك في قاعدة البيانات.")
                return

        if command.startswith("رفع مستوى"):
            try:
                parts = command.split()
                lvl_to_add = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 10
                cost = (lvl_to_add // 10) * 500
                if cost < 500: cost = 500

                if current_money >= cost:
                    db_manager.update_money(user_id, -cost)
                    db_manager.update_level(user_id, lvl_to_add)
                    bot.reply_to(m, f"🆙 تم رفع مستواك بمقدار {lvl_to_add}.\n💸 الخصم: {cost} ذهبة.")
                else:
                    bot.reply_to(m, "❌ ذهبك لا يكفي!")
            except:
                bot.reply_to(m, "⚠️ استخدم الصيغة: شراء رفع مستوى 10")
            return

        if command in prices:
            price = prices[command]
            if current_money >= price:
                db_manager.update_money(user_id, -price)
                bot.reply_to(m, f"✅ تم شراء {command}!\n💰 رصيدك المتبقي: {current_money - price}")
            else:
                bot.reply_to(m, f"❌ رصيدك {current_money} لا يكفي.")
