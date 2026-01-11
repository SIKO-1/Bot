// cmd_balance.js
const { get_user_gold } = require('./db_manager');

const COMMANDS = ["فلوسي", "فلوس", "رصيدي", "رصيدي"];

function handle(bot, ctx) {
    const text = ctx.message?.text?.trim();
    if (!text || !COMMANDS.includes(text)) return;

    const uid = ctx.from.id;
    const gold = get_user_gold(uid);

    ctx.reply(`💰 رصيدك الحالي: ${gold} ذهب`);
}

module.exports = { handle };
