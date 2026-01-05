import os
import telebot
import importlib.util
import traceback
import db_manager
from operator import itemgetter

# ======================
# الإعدادات
# ======================
TOKEN = os.getenv("BOT_TOKEN")
DEV_ID = 5860391324
BOT_ENABLED = True  # متغير عالمي لإطفاء/تشغيل البوت

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN)  # بدون parse_mode لتجنب أخطاء HTML

cmd_modules = {}
game_modules = {}
module_errors = {}

# ======================
# تحميل الموديولات
# ======================
def load_modules():
    global cmd_modules, game_modules, module_errors

    cmd_modules.clear()
    game_modules.clear()
    module_errors.clear()

    base_path = os.path.dirname(__file__)

    for filename in os.listdir(base_path):
        if not filename.endswith(".py"):
            continue
        if filename.startswith("__") or filename == "bot.py":
            continue

        module_name = filename[:-3]
        file_path = os.path.join(base_path, filename)

        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "handle"):
                if filename.startswith("cmd_"):
                    cmd_modules[module_name] = module
                elif filename.startswith("game_"):
                    game_modules[module_name] = module

        except Exception as e:
            module_errors[filename] = str(e)
            try:
                bot.send_message(
                    DEV_ID,
                    f"⚠️ خطأ في تحميل الملف:\n{filename}\n\n{e}"
                )
            except:
                pass

# ======================
# أوامر البداية وتحديث الموديولات
# ======================
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 البوت شغال\n"
        "• كل الأوامر موجودة في cmd_*\n"
        "• كل الألعاب موجودة في game_*\n"
        "• اكتب: تحديث"
    )

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "تحديث")
def update_files(message):
    if message.from_user.id != DEV_ID:
        bot.reply_to(message, "❌ هذا الأمر للمطور فقط")
        return

    load_modules()

    report = "🔄 تم تحديث الموديولات\n\n"
    report += "✅ CMD:\n"
    report += "\n".join(cmd_modules.keys()) or "— لا يوجد"
    report += "\n\n🎮 GAME:\n"
    report += "\n".join(game_modules.keys()) or "— لا يوجد"

    if module_errors:
        report += "\n\n⚠️ أخطاء:\n"
        for f, e in module_errors.items():
            report += f"\n• {f}: {e}"

    bot.send_message(message.chat.id, report)

# ======================
# Dispatcher مع الصمت العقابي واطفاء/تشغيل البوت
# ======================
def dispatch_message(message):
    global BOT_ENABLED
    uid = message.from_user.id
    text = message.text.strip() if message.text else ""

    # ======= أوامر المطور لإطفاء / تشغيل =======
    if uid == DEV_ID:
        if text == "اطفاء":
            BOT_ENABLED = False
            bot.reply_to(message, "🔴 تم إطفاء البوت بأمر الإمبراطور.")
            return
        if text == "تشغيل":
            BOT_ENABLED = True
            bot.reply_to(message, "🟢 عاد البوت للحياة بأمر الإمبراطور.")
            return

    # ======= إذا البوت مطفأ =======
    if not BOT_ENABLED:
        return

    # ======= صمت عقابي للمحظورين =======
    if db_manager.is_user_banned(uid):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        return

    # ======= أوامر المطور: سحب رصيد أو احصائيات أو تصنيف =======
    if uid == DEV_ID and text:
        parts = text.split()
        cmd = parts[0].lower()

        # ----- احصائيات -----
        if cmd == "احصائيات":
            all_users = db_manager.users.find()
            report = "╔═════════════════╗\n"
            report += "  👑 إحصائيات المستخدمين الإمبراطوريين\n"
            report += "╚═════════════════╝\n\n"
            report += f"عدد المستخدمين الكلي: {db_manager.get_all_users_count()}\n\n"
            report += "━━━━━━━━━━━━━━━\n"
            report += "📊 احصائيات بعض المستخدمين:\n"
            for u in all_users:
                name = u.get("name") or "غير معروف"
                username = f"@{u.get('username')}" if u.get("username") else "لا يوجد"
                gold = u.get("gold", 0)
                bank = u.get("bank", 0)
                banned = "✅" if u.get("banned") else "❌"
                report += f"• {name} / {username} / ذهب: {gold} / بنك: {bank} / محظور: {banned}\n"
            bot.reply_to(message, report)
            return

        # ----- سحب رصيد -----
        if cmd == "سحب" and len(parts) >= 3:
            target_uid = parts[1]
            amount = int(parts[2])
            # نبحث عن المستخدم بالـ uid
            try:
                target_uid = int(target_uid)
                user = db_manager._get_user(target_uid)
                db_manager.update_user_gold(target_uid, -amount)
                bot.reply_to(message, f"💸 تم سحب {amount} ذهب من {user.get('name') or 'غير معروف'} / @{user.get('username') or 'لا يوجد'}")
            except Exception as e:
                bot.reply_to(message, f"❌ حدث خطأ: {e}")
            return

        # ----- تصنيف -----
        if cmd == "تصنيف":
            # أغنى 5 أشخاص
            users_sorted = sorted(db_manager.users.find(), key=lambda x: x.get("gold",0), reverse=True)
            top5_rich = users_sorted[:5]

            # أكثر 5 متفاعلين
            users_sorted_usage = sorted(db_manager.users.find(), key=lambda x: x.get("total_messages",0), reverse=True)
            top5_active = users_sorted_usage[:5]

            report = "╔═════════════════╗\n"
            report += "   قائمة التصنيف\n"
            report += "╚═════════════════╝\n\n"

            report += "أغنى 5 أشخاص بالبوت:\n\n"
            for i, u in enumerate(top5_rich, start=1):
                name = u.get("name") or "غير معروف"
                username = f"@{u.get('username')}" if u.get("username") else "لا يوجد"
                gold = u.get("gold", 0)
                report += f"{i}- {name} / {username} / ذهب: {gold}\n"
            report += "\n━━━━━━━━━━━━━━\n"
            report += "أكثر 5 أشخاص متفاعلين:\n\n"
            for i, u in enumerate(top5_active, start=1):
                name = u.get("name") or "غير معروف"
                username = f"@{u.get('username')}" if u.get("username") else "لا يوجد"
                total_msg = u.get("total_messages", 0)
                report += f"{i}- {name} / {username} / رسائل: {total_msg}\n"
            report += "\n━━━━━━━━━━━━━━━"
            bot.reply_to(message, report)
            return

    # ======= تمرير الرسالة للموديولات -----
    try:
        for module in cmd_modules.values():
            module.handle(bot, message)
        for module in game_modules.values():
            module.handle(bot, message)
    except Exception as e:
        traceback.print_exc()
        try:
            bot.send_message(DEV_ID, f"⚠️ خطأ من المستخدم {uid}:\n{e}")
        except:
            pass

# ======================
# Handler عام
# ======================
@bot.message_handler(func=lambda m: True)
def main_handler(message):
    dispatch_message(message)

# ======================
# تشغيل البوت
# ======================
if __name__ == "__main__":
    load_modules()
    print("🤖 البوت جاهز للعمل")
    bot.infinity_polling()
