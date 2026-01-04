import time
import threading
import random
import db_manager

# المعرف الخاص بك يا صاحب السيادة
ADMIN_ID = 5860391324

# مخزن لإدارة الحدث في جميع المجموعات
active_chats = {} 

def register_handlers(bot):
    
    @bot.message_handler(commands=['خصم'])
    def broadcast_duel(m):
        # التحقق من أن القائم بالأمر هو الإمبراطور فقط
        if m.from_user.id != ADMIN_ID:
            return bot.reply_to(m, "هذا النذير لا يطلقه إلا الإمبراطور.")

        # قائمة المجموعات (يجب أن تكون مخزنة في قاعدة بياناتك عند انضمام البوت لها)
        # هنا سنفترض وجود دالة تجلب كل معرفات المجموعات
        all_groups = db_manager.get_all_active_chats() 

        response = (
            "╔═════════════════╗\n"
            "    نذير الحرب العام \n"
            "╚═════════════════╝\n\n"
            "أيها المحاربون في شتى بقاع الأرض\n"
            "لقد استدعى الإمبراطور الخصم المجهول الآن\n"
            "الاسم: UNKNOWN\n\n"
            "أمامكم ثلاثون ثانية لإثبات فصاحتكم\n"
            "الكلمة هي سلاحكم الحاد.. ابدأوا الهجوم\n"
            "━━━━━━━━━━━━━━━\n"
            "ساحات القصر مفتوحة الآن للجميع"
        )

        for chat_id in all_groups:
            try:
                bot.send_message(chat_id, response)
                active_chats[chat_id] = {"start_time": time.time(), "participants": []}
                # جدولة نهاية الحدث لكل مجموعة بشكل مستقل
                threading.Timer(30.0, end_broadcast_duel, [bot, chat_id]).start()
            except:
                continue

    @bot.message_handler(func=lambda m: m.chat.id in active_chats)
    def handle_global_attacks(m):
        chat_data = active_chats.get(m.chat.id)
        if not chat_data:
            return

        elapsed = time.time() - chat_data["start_time"]
        if elapsed > 30:
            return

        word = m.text.strip()
        word_len = len(word)
        
        # تحليل الهجوم بأسلوب ملكي
        success_rate = random.randint(1, 100)
        if success_rate > 40:
            damage = min(99, (word_len * 5) + random.randint(1, 20))
            attack_msg = (
                "ضربة موفقة\n"
                f"المحارب: {m.from_user.first_name}\n"
                f"السلاح: {word}\n"
                f"قوة الاختراق: {damage}%\n"
                "الحالة: هجوم ناجح"
            )
            chat_data["participants"].append({"name": m.from_user.first_name, "score": damage})
        else:
            attack_msg = (
                "هجوم فاشل\n"
                "السبب: ارتباك في ساحة الوغى\n"
                "الخصم يضحك من ضعف الحيلة"
            )
        bot.reply_to(m, attack_msg)

def end_broadcast_duel(bot, chat_id):
    if chat_id in active_chats:
        participants = active_chats[chat_id]["participants"]
        del active_chats[chat_id]
        
        if not participants:
            result_text = "خسارة.. سقطت هذه المقاطعة في يد الخصم"
        else:
            total_damage = sum(p['score'] for p in participants)
            if total_damage > 200:
                result_text = "فوز ساحق.. دُحر الخصم بفضل فرسانكم"
            else:
                result_text = "تعادل.. انسحب الخصم ليعيد الكرة لاحقاً"

        summary = (
            "╔═════════════════╗\n"
            "    ختام الملحمة الكبرى \n"
            "╚═════════════════╝\n\n"
            f"النتيجة في هذه الساحة: {result_text}\n"
            "━━━━━━━━━━━━━━━\n"
            "انقشع الضباب واختفى الخصم.. انتهى الحدث"
        )
        bot.send_message(chat_id, summary)
