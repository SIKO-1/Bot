// ملف: cmd_inventory.js
const COMMANDS = ["مخزوني", "مقتنياتي"];
const db_manager = require("./db_manager"); // استدعاء مدير قاعدة البيانات

async function handle(bot, msg) {
    if (!msg.text) return;

    const text = msg.text.trim();
    if (!COMMANDS.includes(text)) return;

    const uid = msg.from.id;
    const inv = await db_manager.getInventory(uid);

    if (!inv || inv.length === 0) {
        bot.sendMessage(msg.chat.id, "📦 مخزونك فارغ حالياً");
        return;
    }

    const invText = inv.map(item => `- ${item}`).join("\n");
    const response = `📦 مخزونك الحالي:\n${invText}`;
    bot.sendMessage(msg.chat.id, response);
}

module.exports = { handle };
