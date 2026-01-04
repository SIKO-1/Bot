import os
import sys
import telebot

# الأيدي الخاص بك يا إمبراطور
ADMIN_ID = 5860391324

def register_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text in ["رست", "إعادة تشغيل", "restart"])
    def restart_process(message):
        # التحقق من أن الآمر هو الإمبراطور
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "❌ هذا الأمر مخصص للإمبراطور فقط لإدارة شؤون الدولة!")
            return

        bot.reply_to(message, "⚙️ **جاري إعادة تشغيل قلب الإمبراطورية...**\nسأعود للخدمة خلال ثوانٍ.")
        
        # إنهاء العملية الحالية وتشغيل الملف من جديد
        # هذا الأمر سيقوم بإغلاق البوت وتشغيله فوراً
        try:
            os.execv(sys.executable, ['python'] + sys.argv)
        except:
            # لضمان العمل على مختلف الأنظمة (الاستضافة أو الحاسوب)
            os.execv(sys.executable, [sys.executable] + sys.argv)

