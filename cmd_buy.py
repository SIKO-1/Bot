import telebot
# هنا نفترض وجود ملف db_manager للتعامل مع السحابة
from db_manager import get_user_gold, update_user_gold, add_item_to_inventory 

def register_handlers(bot):
    @bot.message_handler(func=lambda message: message.text.startswith("شراء "))
    def buy_item(message):
        user_id = message.from_user.id
        # استخراج اسم الأداة من الرسالة
        item_name = message.text.replace("شراء ", "").strip()
        
        # قائمة الأسعار الرسمية [cite: 2026-01-02]
        prices = {
            "درع الحصانة": 3000,
            "عفو شامل": 5000,
            "تغيير الهوية": 1000,
            "مضاعف الأرباح": 10000,
            "صندوق الحظ": 1000,
            "الكنز": 1000,
            "عيدية": 200,
            "رسالة مثبتة": 100,
            "بايو": 1000
        }

        if item_name in prices:
            price = prices[item_name]
            user_gold = get_user_gold(user_id) # جلب الذهب من MongoDB
            
            if user_gold >= price:
                # عملية الخصم والإضافة
                new_gold = user_gold - price
                update_user_gold(user_id, new_gold)
                add_item_to_inventory(user_id, item_name) # تذهب للمعرض تلقائياً
                
                bot.reply_to(message, f"✅ تمت عملية الشراء بنجاح يا إمبراطور!\n💰 تم خصم {price} ذهبة.\n🖼️ الأداة الآن في معرضك الشخصي.")
            else:
                bot.reply_to(message, f"❌ رصيدك غير كافٍ! تحتاج إلى {price} ذهبة.")
        else:
            bot.reply_to(message, "⚠️ هذه الأداة غير موجودة في المتجر، تأكد من الاسم.")
