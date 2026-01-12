# bot.py
import os
import sys
import importlib
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# ======================
# إعداد البيئة
# ======================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN غير موجود")

# ======================
# المطورين
# ======================
DEV_IDS = [5860391324, 7076215547, 7855813063]  # ضع هنا كل المطورين

# ======================
# قاعدة البيانات
# ======================
import db_manager
db_manager.init_db() if hasattr(db_manager, "init_db") else None

# ======================
# تحميل الموديولات ديناميكياً
# ======================
cmd_modules = {}
game_modules = {}
module_errors = {}

def load_modules():
    global cmd_modules, game_modules, module_errors
    cmd_modules.clear()
    game_modules.clear()
    module_errors.clear()

    base_path = Path(__file__).parent
    print("📦 جاري تحميل الموديولات...")

    for file in base_path.glob("*.py"):
        if file.name in ["bot.py", "db_manager.py"]:
            continue
        module_name = file.stem
        try:
            spec = importlib.import_module(module_name)
            importlib.reload(spec)
            if hasattr(spec, "handle"):
                if module_name.startswith("cmd_"):
                    cmd_modules[module_name] = spec
                elif module_name.startswith("game_"):
                    game_modules[module_name] = spec
            print(f"✅ تم تحميل: {module_name}")
        except Exception as e:
            module_errors[module_name] = str(e)
            print(f"⚠️ خطأ تحميل {module_name}: {e}")
            for dev_id in DEV_IDS:
                try:
                    bot = Bot(BOT_TOKEN)
                    bot.send_message(dev_id, f"⚠️ خطأ تحميل:\n{module_name}\n{str(e)}")
                except:
                    pass

load_modules()

# ======================
# أدوات مساعدة
# ======================
def is_developer(uid):
    return uid in DEV_IDS

# ======================
# أوامر أساسية
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 البوت شغال وبكامل الهيبة.")

async def update_modules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_developer(uid):
        return await update.message.reply_text("❌ هذا الأمر للمطورين فقط")
    load_modules()
    reply = "🔄 تم تحديث الموديولات\n\n✅ CMD:\n"
    reply += "\n".join(cmd_modules.keys()) or "—"
    reply += "\n\n🎮 GAME:\n"
    reply += "\n".join(game_modules.keys()) or "—"
    if module_errors:
        reply += "\n\n⚠️ أخطاء:\n"
        for f, e in module_errors.items():
            reply += f"• {f}: {e}\n"
    await update.message.reply_text(reply)

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_developer(uid):
        await update.message.reply_text("🛑 يتم إيقاف البوت...")
        sys.exit(0)

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_developer(uid):
        await update.message.reply_text("♻️ إعادة تشغيل...")
        os.execv(sys.executable, ["python"] + sys.argv)

# ======================
# التعامل مع الرسائل النصية
# ======================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for module in cmd_modules.values():
        if hasattr(module, "handle"):
            try:
                await module.handle(update, context, db_manager, DEV_IDS)
            except Exception as e:
                print("⚠️ خطأ CMD:", e)
    for module in game_modules.values():
        if hasattr(module, "handle"):
            try:
                await module.handle(update, context, db_manager, DEV_IDS)
            except Exception as e:
                print("⚠️ خطأ GAME:", e)

# ======================
# التعامل مع أزرار Inline
# ======================
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for module in cmd_modules.values():
        if hasattr(module, "handle_callback"):
            try:
                await module.handle_callback(update, context, db_manager, DEV_IDS)
            except Exception as e:
                print("⚠️ خطأ Callback:", e)

# ======================
# تشغيل البوت
# ======================
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("update_modules", update_modules))
app.add_handler(CommandHandler("shutdown", shutdown))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
app.add_handler(CallbackQueryHandler(handle_callback))

print("🚀 البوت شغال وبكامل الهيبة")
app.run_polling()
