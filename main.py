import os
import importlib
from telegram.ext import ApplicationBuilder

def main():
    # جلب التوكن من Variables في ريلوي
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    # ميزة ذكية: إضافة أي ملف يبدأ بكلمة 'cmd_' تلقائياً
    for file in os.listdir():
        if file.startswith("cmd_") and file.endswith(".py"):
            module_name = file[:-3]
            module = importlib.import_module(module_name)
            if hasattr(module, "handler"):
                app.add_handler(module.handler)

    print("العقل يعمل.. تم ربط ملفات الأوامر")
    app.run_polling()

if __name__ == '__main__':
    main()
