@bot.message_handler(func=lambda message: message.text.startswith("شراء "))
def buy_item(message):
    try:
        user_id = message.from_user.id
        item_name = message.text.replace("شراء ", "").strip()
        
        # الأسعار التي حددتها [cite: 2026-01-02]
        prices = {"درع": 3000, "درع الحصانة": 3000, "عفو": 5000, "بايو": 1000} 
        
        if item_name in prices:
            price = prices[item_name]
            user_gold = get_user_gold(user_id) # جلب الذهب من السحابة

            if user_gold < price:
                return bot.reply_to(message, f"❌ رصيدك ({user_gold}) لا يكفي لشراء {item_name}!")

            # --- هنا تبدأ منطقة الخطر التي تسبب الصمت ---
            # 1. الخصم من السحابة
            update_user_gold(user_id, user_id, -price) 
            # 2. الإضافة للمعرض تلقائياً
            add_to_inventory(user_id, item_name) 
            
            # 3. الرد الحتمي (ضروري جداً)
            bot.reply_to(message, f"✅ تم الشراء بنجاح يا إمبراطور!\n🛡️ أداة {item_name} أصبحت في معرضك الآن.\n💰 رصيدك المتبقي: {user_gold - price}")
        
        else:
            bot.reply_to(message, "⚠️ هذا الغرض غير موجود في قائمة المتجر.")

    except Exception as e:
        # إذا حدث أي خطأ برمي، البوت سيخبرك به هنا بدلاً من الصمت
        bot.reply_to(message, f"⚠️ حدث خطأ تقني أثناء الشراء: {e}")
