// cmd_users_admin.js
const db_manager = require('./db_manager');

const COMMANDS = ["ادارة_المستخدمين", "المستخدمين"];
const MAX_MSG_LENGTH = 4000; // الحد الأقصى لرسائل Telegram

// قائمة المطورين المصرح لهم
const DEV_IDS = [5860391324, 123456789, 987654321]; // ضيف كل المطورين هنا

async function handle(ctx) {
    const uid = ctx.from.id;
    const text = ctx.message.text.trim();

    if (!COMMANDS.includes(text)) return;

    if (!DEV_IDS.includes(uid)) {
        return ctx.reply("❌ هذا الأمر للمطورين فقط");
    }

    const users = await db_manager.users.find({}).toArray();
    const total = users.length;

    const banned = [];
    const active = [];

    for (const user of users) {
        const user_id = user.uid;
        const gold = user.gold || 0;
        const bank = user.bank || 0;
        const is_banned = user.banned || false;

        const info = `- ID: ${user_id} | 💰 ${gold} | 🏦 ${bank}`;
        if (is_banned) banned.push(info + " | 🚫 محظور");
        else active.push(info);
    }

    const text_header = 
`╔═════════════════╗
  أهلاً بك يا ${ctx.from.first_name} في إدارة المستخدمين
╚═════════════════╝

👥 عدد المستخدمين الكلي: ${total}

🚫 المحظورين:
`;

    const text_banned = banned.length ? banned.join("\n") : "— لا يوجد —";
    const text_active = "\n\n✅ غير المحظورين:\n" + (active.length ? active.join("\n") : "— لا يوجد —");

    const full_text = text_header + text_banned + text_active;

    // تقسيم الرسالة لو تجاوزت الحد
    for (let i = 0; i < full_text.length; i += MAX_MSG_LENGTH) {
        await ctx.reply(full_text.slice(i, i + MAX_MSG_LENGTH));
    }
}

module.exports = { handle };
