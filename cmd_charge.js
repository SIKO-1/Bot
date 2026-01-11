// ملف: cmd_charge.js
const db = require("./db_manager");

// 🆔 ايديات المطورين (من env)
const DEV_IDS = process.env.DEV_IDS
    ? process.env.DEV_IDS.split(",").map(id => parseInt(id.trim()))
    : [];

// الأوامر
const COMMANDS = ["شحن"];

async function handle(bot, ctx) {
    if (!ctx.message || !ctx.message.text) return;

    const text = ctx.message.text.trim();
    const parts = text.split(" ");

    if (!COMMANDS.includes(parts[0])) return;

    const uid = ctx.from.id;

    // 🔒 حماية: مطورين فقط
    if (!DEV_IDS.includes(uid)) {
        return ctx.reply("❌ هذا الأمر مخصص للمطورين فقط");
    }

    // =====================
    // 🧵 حالة الرد على شخص
    // =====================
    if (ctx.message.reply_to_message) {
        if (parts.length !== 2) {
            return ctx.reply("⚠️ الصيغة:\nشحن <الكمية>");
        }

        const amount = parseInt(parts[1]);
        if (isNaN(amount)) {
            return ctx.reply("❌ الكمية لازم تكون رقم");
        }
        if (amount <= 0) {
            return ctx.reply("❌ الكمية لازم تكون أكبر من صفر");
        }

        const target = ctx.message.reply_to_message.from;
        const newGold = await db.update_user_gold(target.id, amount);

        return ctx.reply(
            `✅ تم الشحن بنجاح\n\n` +
            `👤 الاسم: ${target.first_name}\n` +
            `🆔 ID: ${target.id}\n` +
            `💰 المبلغ: +${amount}\n` +
            `✨ الرصيد الحالي: ${newGold}`
        );
    }

    // =====================
    // 🆔 حالة ID مباشر
    // =====================
    if (parts.length !== 3) {
        return ctx.reply(
            "⚠️ الصيغة الصحيحة:\n" +
            "شحن <ID> <الكمية>\n" +
            "أو رد على الشخص واكتب:\n" +
            "شحن <الكمية>"
        );
    }

    const targetId = parseInt(parts[1]);
    const amount = parseInt(parts[2]);

    if (isNaN(targetId) || isNaN(amount)) {
        return ctx.reply("❌ ID والكمية لازم يكونوا أرقام");
    }
    if (amount <= 0) {
        return ctx.reply("❌ الكمية لازم تكون أكبر من صفر");
    }

    const newGold = await db.update_user_gold(targetId, amount);

    return ctx.reply(
        `✅ تم شحن الحساب بنجاح\n\n` +
        `🆔 ID: ${targetId}\n` +
        `💰 المبلغ: +${amount}\n` +
        `✨ الرصيد الحالي: ${newGold}`
    );
}

module.exports = { handle };
