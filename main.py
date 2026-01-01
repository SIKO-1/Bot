import os
import importlib
import logging
from telegram.ext import ApplicationBuilder

logging.basicConfig(level=logging.INFO)

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("❌ BOT_TOKEN غير موجود!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # جلب قائمة الملفات في المجلد الحالي
    files = [f for f in os.listdir('.') if f.startswith("cmd_") and f.endswith(".py")]
    print(f"📂 الملفات التي تم العثور عليها: {files}")

    for file in files:
        module_name = file[:-3]
        try:
            # محاولة استيراد الملف
            module = importlib.import_module(module_name)
            found_handler = False
            for attr in dir(module):
                if attr.endswith("_handler"):
                    handler = getattr(module, attr)
                    app.add_handler(handler)
                    found_handler = True
            
            if found_handler:
                print(f"✅ تم تحميل: {file}")
            else:
                print(f"⚠️ ملف {file} لا يحتوي على متغير ينتهي بـ _handler")
                
        except Exception as e:
            print(f"❌ خطأ أثناء تحميل {file}: {e}")

    print("🚀 إمبراطورية كرار انطلقت الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
