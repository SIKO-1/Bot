import sqlite3

# دالة محلية للتعامل مع القاعدة مباشرة لضمان عدم حدوث خطأ استيراد
def manage_db(user_id, amount=0, mode="get"):
    try:
        conn = sqlite3.connect('database.db') # تأكد أن اسم ملف القاعدة database.db أو غيره
        cursor = conn.cursor()
        
        if mode == "get":
            cursor.execute("SELECT money FROM users WHERE user_id = ?", (user_id,))
            res = cursor.fetchone()
            conn.close()
            return res[0] if res else 0
        
        elif mode == "update":
            cursor.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (amount, user_id))
            conn.commit()
            conn.close()
            
        elif mode == "level":
            cursor.execute("UPDATE users SET level = level + ? WHERE user_id = ?", (amount, user_id))
            conn.commit()
            conn.close()
    except:
        return 0

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
        
        # الأسعار التي حددتها [cite: 2026-01-02]
        prices = {
            "درع": 3000, "عفو": 5000, "هوية": 1000, 
            "مضاعفة": 10000, "صندوق الحظ": 1000, "الكنز": 1000, 
            "عيدية": 200, "رسالة مثبتة": 100, "بايو صديق": 1000
        }

        current_money = manage_db(user_id, mode="get")

        if command.startswith("رفع مستوى"):
            try:
                parts = command.split()
                lvl_to_add = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 10
                cost = (lvl_to_add // 10) * 500
                if cost < 500: cost = 500

                if current_money >= cost:
                    manage_db(user_id, -cost, mode="update")
                    manage_db(user_id, lvl_to_add, mode="level")
                    bot.reply_to(m, f"🆙 تم رفع مستواك بمقدار {lvl_to_add}.\n💸 تم خصم {cost} ذهبة.")
                else:
                    bot.reply_to(m, f"❌ رصيدك ({current_money}) لا يكفي!")
            except:
                bot.reply_to(m, "⚠️ استخدم: شراء رفع مستوى 10")
            return

        if command in prices:
            price = prices[command]
            if current_money >= price:
                manage_db(user_id, -price, mode="update")
                bot.reply_to(m, f"✅ تم شراء {command} بنجاح!\n💰 المتبقي: {current_money - price}")
            else:
                bot.reply_to(m, f"❌ رصيدك {current_money} لا يكفي.")
