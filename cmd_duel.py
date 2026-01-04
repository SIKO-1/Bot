import time
import threading
import random
import db_manager

# القائمة الملكية للمعرفات
ADMIN_ID = 5860391324
duel_active = False
active_chats = {}

def register_handlers(bot):
    
    @bot.message_handler(commands=['الخصم'])
    def broadcast_duel(m):
        global duel_active
        # لا يطلق بوق الحرب إلا الإمبراطور
        if m.from_user.id != ADMIN_ID:
            return bot.reply_to(m, "هذا النداء لا يطلقه إلا صاحب العرش.")

        if duel_active:
            return bot.reply_to(m, "المعركة قائمة بالفعل في أرجاء الإمبراطورية.")

        duel_active = True
        # جلب المجموعات من السحاب (تأكد من وجود دالة get_all_active_chats في db_manager)
        all_groups = db_manager.get_all_active_chats() 

        announcement = (
            "╔═════════════════╗\n"
            "    نذير الحرب الشامل \n"
            "╚═════════════════╝\n\n"
            "أيها المحاربون.. استعدوا للهجوم\n"
            "الخصم: UNKNOWN\n"
            "المهلة: 30 ثانية\n\n"
            "اكتبوا أي كلمة الآن لتكون سلاحكم\n"
            "━━━━━━━━━━━━━━━\n"
            "المواجهة بدأت الآن"
        )

        for chat_id in all_groups:
            try:
                bot.send_message(chat_id, announcement)
                active_chats[chat_id] = {"start_time": time.time(), "damage": 0}
            except:
                continue

        # إنهاء الملحمة بعد 30 ثانية
        threading.Timer(30.0, end_duel_globally, [bot]).start()

    @bot.message_handler(func=lambda m: duel_active and m.chat.id in active_chats)
    def handle_attacks(m):
        # تحليل الهجوم بأسلوب ملكي
        word = m.text.strip()
        if len(word) < 2: return

        # حساب الضرر بناءً على طول الكلمة وسرعتها
        damage = min(95, (len(word) * 4) + random.randint(1, 15))
        
        # تسجيل الضرر للمجموعة
        active_chats[m.chat.id]["damage"] += damage
        
        # رد سريع على الهجوم
        if random.random() > 0.4: # لإضفاء عشوائية ذكية
            bot.reply_to(m, f"هجوم ناجح\nالسلاح: {word}\nالضرر: {damage}%")
        else:
            bot.reply_to(m, "هجوم فاشل.. لقد تفادى الخصم ضربتك بسخرية")

def end_duel_globally(bot):
    global duel_active, active_chats
    
    for chat_id, data in active_chats.items():
        total = data["damage"]
        if total > 150:
            res = "فوز ساحق.. تم سحق الخصم وتشتيت قواه"
        elif total > 50:
            res = "تعادل.. انسحب الخصم ليعيد الكرة لاحقاً"
        else:
            res = "خسارة.. لقد كانت كلماتكم أضعف من دروع الخصم"

        summary = (
            "╔═════════════════╗\n"
            "    بيان ختام المعركة \n"
            "╚═════════════════╝\n\n"
            f"النتيجة النهائية: {res}\n"
            "━━━━━━━━━━━━━━━\n"
            "انتهت الملحمة.. اختفى الخصم في الظلال"
        )
        try:
            bot.send_message(chat_id, summary)
        except: pass

    # تصفير البيانات للمعركة القادمة
    active_chats = {}
    duel_active = False
