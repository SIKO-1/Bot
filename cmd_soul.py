import time
import db_manager
from datetime import datetime

# لحظة انبثاق الروح (بداية التشغيل)
START_TIME = time.time()
# عداد الأخطاء الواقعي
INTERNAL_ERRORS = 0

def register_handlers(bot):
    EMPEROR_ID = 5860391324

    # 1. إرسال برقية استيقاظ فور تشغيل البوت
    try:
        bot.send_message(EMPEROR_ID, "مراسم الانبعاث: استعادت روح الإمبراطورية وعيها الكامل الآن.")
    except:
        pass

    # 2. دالة التحقق من النخبة
    def is_authorized(user_id):
        if user_id == EMPEROR_ID: return True
        user_data = db_manager.get_user(user_id)
        return user_data and user_data.get("rank") == "admin"

    # 3. أمر "روح" لاستنطاق السجل
    @bot.message_handler(func=lambda m: m.text == "روح")
    def bot_soul_status(m):
        global INTERNAL_ERRORS
        
        # حارس البوابة (المنفيين لا يرون شيئاً)
        if db_manager.get_user(m.from_user.id).get("banned"): return
        
        # حصر الاطلاع للأسياد
        if not is_authorized(m.from_user.id):
            return bot.reply_to(m, "ويحك. أسرار الروح لا تُباح إلا لمن اعتلى العرش.")

        # حساب زمن الصمود
        uptime_seconds = int(time.time() - START_TIME)
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        
        # استدعاء البيانات الحقيقية من الخزينة
        total_users = db_manager.get_total_users_count()
        banned_users = db_manager.get_banned_users_count()
        total_msgs = db_manager.get_total_messages()

        soul_report = (
            "سِجِلُّ رُوحِ الإِمْبِرَاطُورِيَّةِ\n"
            "-------------------------------\n\n"
            "مقام الكيان: نشط\n"
            f"زمن الصمود: {days} يوم، {hours} ساعة، {minutes} دقيقة\n\n"
            "إحصائيات الديوان العالي:\n"
            f"النفوس المقيدة: {total_users}\n"
            f"الرعايا المنبوذون: {banned_users}\n"
            f"إجمالي صرخات الرعايا: {total_msgs}\n\n"
            "التقرير الباطني للحالة:\n"
            f"الشوائب البرمجية المرصودة: {INTERNAL_ERRORS}\n"
            "الاستقرار الفني: مطلق\n"
            "-------------------------------\n"
            "الروح فانية، والسيادة للإمبراطور وحده.\n"
            f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        bot.reply_to(m, soul_report)

# دالة خارجية لزيادة عداد الأخطاء من الملف الرئيسي
def log_error():
    global INTERNAL_ERRORS
    INTERNAL_ERRORS += 1
