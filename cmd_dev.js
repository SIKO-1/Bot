// ملف: cmd_dev.js

// هذا الأمر خاص بالمطورين فقط
const COMMANDS = ["اشعار"];

function handle(bot, ctx, db) {
    if (!ctx.message || !ctx.message.text) return;

    const text = ctx.message.text.trim();
    const uid = ctx.from.id;

    // جلب قائمة المطورين من env (نفس bot.js)
    const DEV_IDS = process.env.DEV_IDS
        ? process.env.DEV_IDS.split(',').map(id => parseInt(id.trim()))
        : [];

    // حماية: مطور فقط
    if (!DEV_IDS.includes(uid)) return;

    // ======================
    // أمر الإشعار الجماعي
    // ======================
    if (text.startsWith("اشعار")) {
        const msg = text.replace("اشعار", "").trim();

        if (!msg) {
            ctx.reply("❌ اكتب نص الإشعار بعد كلمة (اشعار)");
            return;
        }

        const users = db.get_all_users(); // لازم تكون موجودة بالـ db_manager
        let count = 0;

        for (const u of users) {
            try {
                bot.telegram.sendMessage(
                    u.uid,
                    `📢 رسالة من الإدارة:\n\n${msg}`
                );
                count++;
            } catch (e) {
                // تجاهل المستخدمين اللي مسكرين الخاص
            }
        }

        ctx.reply(`✅ تم إرسال الإشعار إلى ${count} مستخدم`);
        return;
    }
}

module.exports = { handle };
