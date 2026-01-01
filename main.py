import os
import importlib
import logging
import asyncio
from telegram.ext import ApplicationBuilder

# إعداد السجلات لمتابعة العمليات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # جلب التوكن من إعدادات ريلوي
    TOKEN = os.environ.get("BOT_TOKEN")
    
    if not TOKEN:
        print("❌ خطأ: لم يتم العثور على BOT_TOKEN في المتغيرات!")
        return

    # بناء التطبيق
    app = ApplicationBuilder().token(TOKEN).build()

    # حلقة البحث عن ملفات الأوامر
    for file in os.listdir():
        if file.startswith("cmd_") and file.endswith(".py"):
            module_name = file[:-3]
            try:
                # استيراد الملف
                module = importlib.import_module(module_name)
                
                # البحث عن أي متغير ينتهي بـ _handler
                found_any = False
                for attr in dir(module):
                    if attr.endswith("_handler"):
                        handler = getattr(module, attr)
                        app.add_handler(handler)
                        found_any = True
                
                if found_any:
                    print(f"✅ تم تحميل: {file}")
            except Exception as e:
                print(f"❌ مشكلة في ملف {file}: {e}")

    print("🚀 إمبراطورية كرار انطلقت الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
