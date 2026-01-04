from telebot import types

EMPEROR_ID = 5860391324  # <--- استبدل بـ ID الحقيقي

ADMIN_TRIGGERS = ["ادارة", "امبراطورية", "ادارة الإمبراطورية", "إمبراطورية"]

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text and m.text.strip().lower() in [t.lower() for t in ADMIN_TRIGGERS])
    def emperor_only_panel(m):
        user_id = m.from_user.id
        user_name = m.from_user.first_name

        if user_id == EMPEROR_ID:
            emperor_tag = f"{user_name}"  # HTML mode safer

            text = (
                "╔═════════════════════════╗\n"
                "      🏰 إدارة الإمبراطورية 🏰\n"
                "╚═════════════════════════╝\n\n"
                f"مرحباً بك يا إمبراطور: {emperor_tag}\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🔹 أقسام الإدارة :\n"
                "┌───────────────────────┐\n"
                "   • كتم / إلغاء كتم\n"
                "   • حظر / إلغاء حظر\n"
                "   • تقيد / إلغاء تقيد\n"
                "   • سجل البوت / روح\n"
                "   • رفع أدمن / تنزيل أدمن\n"
                "   • تحديث ملفات / تحديث الأوامر\n"
                "   • إعادة تشغيل البوت / Reset\n"
                "   • شحن رصيد / تصفير رصيد\n"
                "   • تحويل رصيد بين المستخدمين\n"
                "   • قفل البوت / فتح البوت\n"
                "   • عرض إحصائيات المستخدمين والمراسلات\n"
                "   • إدارة الأوامر المخصصة (عرض/حذف/تعديل)\n"
                "└───────────────────────┘\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "💠 «هيبتك لا تُصنع بالخوف، بل بالعدل الذي يرتجف منه الظالم.»"
            )

            bot.send_message(m.chat.id, text, parse_mode="HTML")
        
        else:
            # أي محاولة من غير الإمبراطور
            bot.reply_to(m, "⚠️ أنت عبد من عباد الإمبراطور، لا تتجرأ وتقول ذلك ثانية!")
            # Logging في الخاص للإمبراطور
            try:
                bot.send_message(EMPEROR_ID, f"⚠️ مستخدم {user_name} [{user_id}] حاول الوصول إلى لوحة الإدارة.")
            except:
                pass
