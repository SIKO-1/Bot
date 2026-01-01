import os
import importlib
import logging
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
        print("خطأ: لم يتم العثور على BOT_TOKEN في المتغيرات!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # حلقة ذكية للبحث في المجلد عن ملفات الأوامر
    for file in os.listdir():
        # يبحث عن الملفات التي تبدأ بـ cmd_ وتنهي بـ .py
        if file.startswith("cmd_") and file.endswith(".py"):
            module_name = file[:-3] # حذف .py من الاسم
            try:
                # استيراد الملف برمجياً
                module = importlib.import_module(module_name)
                
                # البحث عن أي متغير ينتهي بـ _handler داخل الملف
                # هذا يسمح لك بوضع عدة أوامر في ملف واحد
                for attr in dir(module):
                    if attr.endswith("_handler"):
                        handler = getattr(module, attr)
                        app.add_handler(handler)
                
                print(f"✅ تم تحميل الملف بنجاح: {file}")
            except Exception as e:
                print(f"❌ فشل تحميل الملف {file}: {e}")

    print("🚀 إمبراطورية كرار تعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
