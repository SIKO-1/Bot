// cmd_bank.js
const db = require('./db_manager');

const COMMANDS = ["بنك", "رصيد_بنك", "سحب", "ايداع"];

function handle(bot, ctx) {
    const text = ctx.message?.text?.trim();
    if (!text || !COMMANDS.some(cmd => text.startsWith(cmd))) return;

    const uid = ctx.from.id;

    // ===== رصيد البنك =====
    if (["بنك", "رصيد_بنك"].includes(text)) {
        const bank_gold = db.get_user_bank(uid);
        ctx.reply(`🏦 رصيدك في البنك: ${bank_gold} ذهب`);
        return;
    }

    // ===== إيداع =====
    if (text.startsWith("ايداع")) {
        const parts = text.split(" ");
        if (parts.length !== 2 || isNaN(parts[1])) {
            ctx.reply("⚠️ الصيغة: ايداع 500");
            return;
        }

        const amount = parseInt(parts[1]);
        if (db.deposit_to_bank(uid, amount)) {
            ctx.reply(`✅ تم إيداع ${amount} ذهب في البنك`);
        } else {
            ctx.reply("❌ رصيدك لا يكفي");
        }
        return;
    }

    // ===== سحب =====
    if (text.startsWith("سحب")) {
        const parts = text.split(" ");
        if (parts.length !== 2 || isNaN(parts[1])) {
            ctx.reply("⚠️ الصيغة: سحب 300");
            return;
        }

        const amount = parseInt(parts[1]);
        if (db.withdraw_from_bank(uid, amount)) {
            ctx.reply(`✅ تم سحب ${amount} ذهب من البنك`);
        } else {
            ctx.reply("❌ رصيد البنك لا يكفي");
        }
        return;
    }
}

module.exports = { handle };
