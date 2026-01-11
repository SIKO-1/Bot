// ملف: cmd_downgrade.js
const db = require("./db_manager"); // استدعاء db_manager.js

const COMMAND = "تخفيض";

async function handle(bot, ctx) {
    const text = ctx.message.text?.trim();
    if (!text || !text.startsWith(COMMAND)) return;

    const fromUid = ctx.from.id;
    const parts = text.split(" ");

    // ======= تحقق من المطور =======
    if (!db.DEVELOPERS.includes(fromUid)) {
        ctx.reply("❌ هذا الأمر للمطور فقط.");
        return;
    }

    let targetUid, newRank;

    // ======= حالة الرد على شخص =======
    if (ctx.message.reply_to_message) {
        if (parts.length !== 2) {
            ctx.reply("⚠️ الصيغة:\nتخفيض <رقم_الرتبة>");
            return;
        }

        targetUid = ctx.message.reply_to_message.from.id;
        newRank = parseInt(parts[1], 10);
        if (isNaN(newRank)) {
            ctx.reply("❌ رقم الرتبة يجب أن يكون رقمًا.");
            return;
        }
    } 
    // ======= حالة استخدام ID مباشرة =======
    else {
        if (parts.length !== 3) {
            ctx.reply("⚠️ الصيغة:\nتخفيض <ID> <رقم_الرتبة>");
            return;
        }

        targetUid = parseInt(parts[1], 10);
        newRank = parseInt(parts[2], 10);
        if (isNaN(targetUid) || isNaN(newRank)) {
            ctx.reply("❌ الـ ID والرتبة يجب أن يكونوا أرقام.");
            return;
        }
    }

    // ======= تنفيذ التخفيض =======
    try {
        const result = await db.downgradeUserRank(fromUid, targetUid, newRank);
        if (!result.ok) {
            ctx.reply(result.error);
            return;
        }

        ctx.reply(
            `✅ تم التخفيض بنجاح\n` +
            `🔻 الرتبة السابقة: ${result.old_rank}\n` +
            `🔻 الرتبة الحالية: ${result.new_rank}`
        );
    } catch (err) {
        console.log("❌ خطأ أثناء التخفيض:", err.message);
        ctx.reply("❌ حدث خطأ أثناء تنفيذ الأمر.");
    }
}

module.exports = { handle };
