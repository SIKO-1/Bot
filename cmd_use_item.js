// cmd_use_item.js
const db_manager = require('./db_manager');

const COMMANDS_USE = ["استخدم", "استعمل"];

const ITEM_EFFECTS = {
    "سيف الإمبراطور 🔱": async (uid) => await db_manager.update_user_gold(uid, 50),
    "درع الحماية الأسطوري 🛡️": async (uid) => await db_manager.extend_protection(uid, 24*3600),
    "خاتم التفاعل 💍": async (uid) => await db_manager.add_fake_messages(uid, 10),
    "عملة الإمبراطور 💰": async (uid) => await db_manager.update_user_gold(uid, 1000),
    "كتاب الحكمة 📜": async (uid) => await db_manager.add_random_rare_item(uid),
    "خوذة الحكيم 🪖": async (uid) => await db_manager.reduce_gift_cooldown(uid, 0.5),
    "بلورة الزمن ⏳": async (uid) => await db_manager.reset_daily_task(uid)
};

async function handle(ctx) {
    const uid = ctx.from.id;
    const text = ctx.message.text.trim();

    if (!COMMANDS_USE.some(cmd => text.startsWith(cmd))) return;

    const parts = text.split(/\s+(.+)/); // يقسم مرة وحدة فقط
    if (parts.length < 2 || !parts[1].trim()) {
        return ctx.reply("❌ اكتب اسم العنصر الذي تريد استخدامه بعد الأمر");
    }

    const item_name = parts[1].trim();
    const inventory = await db_manager.get_inventory(uid);

    if (!inventory.includes(item_name)) {
        return ctx.reply(`❌ لا يمكنك استخدام هذا العنصر لأنك لا تمتلكه في المخزون.`);
    }

    // تنفيذ التأثير
    const effect_func = ITEM_EFFECTS[item_name];
    if (effect_func) {
        await effect_func(uid);
        await db_manager.remove_from_inventory(uid, item_name);
        return ctx.reply(`✅ استخدمت ${item_name} وتم تطبيق تأثيره!`);
    } else {
        return ctx.reply("❌ هذا العنصر ليس لديه تأثير محدد.");
    }
}

module.exports = { handle };
