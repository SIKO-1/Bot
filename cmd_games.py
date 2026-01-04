import telebot
import db_manager

# الكلمات المفتاحية لفتح قائمة الألعاب
GAME_TRIGGERS = [
    'العاب', 'الألعاب', 'الالعاب', 'لعبات', 'لعبة'
]

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text and m.text.strip().lower() in [g.lower() for g in GAME_TRIGGERS])
    def send_grand_menu(m):
        try:
            # 🛑 الحارس الإمبراطوري: التحقق من سجل المنفيين
            user_info = db_manager.get_user(m.from_user.id)
            if user_info and user_info.get("banned"):
                return # صمت ملكي.. لا استجابة للمنبوذين

            menu_text = (
                "⌔︙قائمة ألعاب الإمبراطورية\n"
                "—————————————\n"
                "⌔︙نرد » لعبة النرد الملكية\n"
                "⌔︙روليت » الروليت بالمعرفات\n"
                "⌔︙نبض » قياس النبض\n"
                "⌔︙مين » خمن من انا\n"
                "⌔︙تخمين » لعبة تخمين الأرقام\n"
                "⌔︙رياضيات» مسائل رياضيات\n"
                "⌔︙حجره » لعبة حجره ورق مقص\n"
                "⌔︙كيبورد » تحدي سرعة الكتابة\n"
                "⌔︙عواصم » لعبة عواصم الدول\n"
                "⌔︙صح » صح أم خطأ\n"
                "⌔︙اربح » من سيربح المليون\n"
                "⌔︙فكك » لعبة جماد حيوان نبات\n"
                "⌔︙عكس » لعبة الكلمات المتناقضة\n"
                "⌔︙اعتراف » لعبة الاعترافات\n"
                "⌔︙لو » لعبة لو خيروك\n"
                "⌔︙xo » لعبة اكس او الشفافة\n"
                "⌔︙فلوس » عرض الرصيد البنكي\n"
                "—————————————\n"
                "💡 اكتب اسم اللعبة لتبدأ المتعة!"
            )

            bot.reply_to(m, menu_text) 

        except Exception as e:
            # أي خطأ يتم إرساله بالخاص للإمبراطور
            bot.send_message(m.chat.id, menu_text)
            try:
                bot.send_message(5860391324, f"❌ خطأ في cmd_games.py مع {m.from_user.id}: {e}")
            except:
                pass
