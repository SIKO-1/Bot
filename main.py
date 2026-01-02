import telebot
import os
import importlib.util

# 1. التوكن الخاص بك
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)

print("--- 🔄 محاولة إنعاش البوت ---")

# 2. قائمة بأسماء ملفات الألعاب التي تريد تشغيلها (تأكد من كتابة الأسماء صح)
# لا تضع .py في الأسماء هنا
games_to_load = ['game_million', 'game_quiz', 'game_smart', 'game_time', 'game_rps', 'game_emoji']

for folder in [".", "plugins"]: # سيبحث في المجلد الرئيسي وفي مجلد plugins
    for game in games_to_load:
        file_path = os.path.join(folder, f"{game}.py")
        if os.path.exists(file_path):
            try:
                spec = importlib.util.spec_from_file_location(game, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(bot)
                    print(f"✅ تم تحميل: {game}")
            except Exception as e:
                print(f"❌ خطأ في ملف {game}: {e}")

# 3. أمر فحص بسيط للتأكد أن البوت حي
@bot.message_handler(commands=['ping'])
def ping(m):
    bot.reply_to(m, "🚀 الإمبراطورية حية وتتنفس!")

if __name__ == "__main__":
    print("🚀 البوت انطلق الآن...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"⚠️ خطأ في التشغيل (Polling): {e}")
