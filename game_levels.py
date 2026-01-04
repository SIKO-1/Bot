import db_manager
import random

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "مستواي")
    def check_level(m):
        try:
            # جلب البيانات من الخزينة السحابية
            level, xp = db_manager.get_user_level(m.from_user.id)
            
            response = (
                "╔═════════════════╗\n"
                "    سجل الوقار الإمبراطوري \n"
                "╚═════════════════╝\n\n"
                f"المحارب: {m.from_user.first_name}\n"
                f"المستوى الحالي: {level}\n"
                f"نقاط الخبرة: {xp}\n"
                "━━━━━━━━━━━━━━━\n"
                "استمر في العطاء ليرتقي شأنك"
            )
            bot.reply_to(m, response)
        except Exception as e:
            print(f"خطأ في عرض المستوى: {e}")

    @bot.message_handler(func=lambda m: True)
    def track_activity(m):
        """رصد النشاط وزيادة الخبرة بحذر شديد"""
        try:
            # استثناء الأوامر والرسائل القصيرة جداً من الرصد
            if m.text and not m.text.startswith(("/", "!", "#")) and len(m.text) > 2:
                # منح نقاط خبرة عشوائية (بين 2 إلى 7)
                added_xp = random.randint(2, 7)
                # تحديث البيانات في السحاب مع حماية من الانهيار
                db_manager.update_user_experience(m.from_user.id, added_xp)
        except Exception as e:
            # طباعة الخطأ في الكونسول فقط دون تعطيل البوت
            print(f"⚠️ خلل في نظام الرصد: {e}")
        
        # أمر ملكي: السماح للرسالة بالمرور للأوامر الأخرى دائماً
        return False 
