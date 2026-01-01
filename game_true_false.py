import random
from telebot import types
from db_manager import get_user, update_user

def register_handlers(bot):
    
    TF_QUESTIONS = [
        {"q": "الحوت يتنفس من الرئتين وليس الخياشيم.", "a": "صح"},
        {"q": "الشمس تدور حول الأرض مرة كل سنة.", "a": "خطأ"},
        {"q": "الطماطم تُعد فاكهة علميًا.", "a": "صح"},
        {"q": "الإنسان يستخدم 10٪ فقط من دماغه.", "a": "خطأ"},
        {"q": "يمكن للبرق أن يضرب المكان نفسه أكثر من مرة.", "a": "صح"},
        {"q": "القمر يملك ضوءًا خاصًا به.", "a": "خطأ"},
        {"q": "الدماغ لا يشعر بالألم.", "a": "صح"},
        {"q": "الذهب يمكن كسره باليد إذا كان نقيًا جدًا.", "a": "صح"},
        {"q": "الزرافة لا تستطيع إصدار أي صوت.", "a": "خطأ"},
        {"q": "الخفاش أعمى تمامًا.", "a": "خطأ"},
        {"q": "الموز ينمو على شجرة.", "a": "خطأ"},
        {"q": "العسل الطبيعي لا يفسد مع الزمن.", "a": "صح"},
        {"q": "انت اعمى.", "a": "صح"},
        {"q": "الدم في جسم الإنسان لونه أزرق.", "a": "خطأ"},
        {"q": "الإنسان يولد بعدد عظام أقل من البالغ.", "a": "خطأ"},
        {"q": "الجلد هو أكبر عضو في جسم الإنسان.", "a": "صح"},
        {"q": "القمر يؤثر على حركة المد والجزر.", "a": "صح"}
        # (يمكنك إضافة باقي الـ 50 هنا بنفس التنسيق)
    ]

    # رسائل سخرية عشوائية للأجوبة الخطأ
    ROASTS = [
        "ما توقعتك بهذا الغباء الصراحة.. 🤡",
        "يا ساتر! المعلومات عندك صفر 📉",
        "حتى جدي يعرف الإجابة، ركز يا بطل! 😂",
        "شكلك كنت نايم في حصة العلوم.. 😴",
        "غلط! روح اقرأ كتب بدل ما تضيع وقتك هنا 📚",
        "تحتاج إعادة ضبط مصنع لعقلك 🧠⚠️"
    ]

    @bot.message_handler(func=lambda m: m.text == "صح")
    def start_tf_game(m):
        item = random.choice(TF_QUESTIONS)
        question_text = f"🧐 **تحدي الصح والخطأ**\n\n- {item['q']}"
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_true = types.InlineKeyboardButton("✅ صح", callback_data=f"tf_صح_{item['a']}_{item['q']}")
        btn_false = types.InlineKeyboardButton("❌ خطأ", callback_data=f"tf_خطأ_{item['a']}_{item['q']}")
        
        markup.add(btn_true, btn_false)
        bot.reply_to(m, question_text, reply_markup=markup, parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("tf_"))
    def handle_tf_answer(call):
        # تقسيم البيانات
        data = call.data.split("_")
        user_choice = data[1]
        correct_answer = data[2]
        question_asked = data[3]
        uid = call.from_user.id
        
        if user_choice == correct_answer:
            points = 50
            new_bal = get_user(uid)["balance"] + points
            update_user(uid, "balance", new_bal)
            bot.edit_message_text(f"✅ **صح يا ذكي!**\n\nربحت {points} نقطة.\n💰 رصيدك: {new_bal}", 
                                  chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            # السخرية الخاصة بسؤال "انت اعمى"
            if "انت اعمى" in question_asked:
                insult = "مو خبرتك؟ يا أعمى! حتى هذي غلطت فيها؟ 🦯🤣"
            else:
                insult = random.choice(ROASTS)
            
            bot.edit_message_text(f"❌ **خطأ!**\n\nالإجابة الصح هي: {correct_answer}\n\n💬 {insult}", 
                                  chat_id=call.message.chat.id, message_id=call.message.message_id)
