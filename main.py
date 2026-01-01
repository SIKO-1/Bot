import os
import importlib
import logging
from telegram.ext import ApplicationBuilder

logging.basicConfig(level=logging.INFO)

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    files = [f for f in os.listdir('.') if f.startswith("cmd_") and f.endswith(".py")]

    for file in files:
        module_name = file[:-3]
        try:
            module = importlib.import_module(module_name)
            for attr in dir(module):
                if attr.endswith("_handler"):
                    handler = getattr(module, attr)
                    
                    # نظام المستويات والبروفايل نضعه في مجموعة 0 (تعمل دائماً)
                    if "profile" in attr or "level" in attr:
                        app.add_handler(handler, group=0)
                    # بقية الأوامر (منيو، رصيد، شوب) في مجموعة 1
                    else:
                        app.add_handler(handler, group=1)
            print(f"✅ تم تحميل: {file}")
        except Exception as e:
            print(f"❌ خطأ في {file}: {e}")

    print("🚀 البوت انطلق بنظام المجموعات...")
    app.run_polling()

if __name__ == '__main__':
    main()
