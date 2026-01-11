// cmd_stats.js
const { _get_user, get_all_users_count, update_user_gold, users } = require('./db_manager');

const COMMANDS = ["احصائيات", "سحب", "تصنيف"];

async function handle(ctx) {
    const text = ctx.message.text.trim();
    const uid = ctx.from.id;

    if (!COMMANDS.some(cmd => text.startsWith(cmd))) return;

    // ======================
    // احصائيات المستخدم
    // ======================
    if (text.startsWith("احصائيات")) {
        const user = await _get_user(uid);
        const gold = user.gold || 0;
        const bank = user.bank || 0;
        const msgs = user.total_messages || 0;
        const daily = user.daily_usage || 0;
        const banned = !user.banned ? "✅" : "❌";

        const name_display = user.name || uid;
        const username_display = user.username ? `@${user.username}` : uid;

        const report = `╔═════════════════╗
أهلاً بك في إدارة المستخدمين
╚═════════════════╝

عدد المستخدمين الكلي: ${await get_all_users_count()}

━━━━━━━━━━━━━━━
معلوماتك:

• الاسم: ${name_display}
• يوزرنيم / UID: ${username_display}
• الذهب: ${gold}
• البنك: ${bank}
• عدد الرسائل الكلي: ${msgs}
• الاستخدام اليومي: ${daily}
• محظور: ${banned}
━━━━━━━━━━━━━━━
`;
        return ctx.reply(report);
    }

    // ======================
    // سحب الذهب
    // ======================
    if (text.startsWith("سحب")) {
        const parts = text.split(" ");
        if (parts.length !== 3) return ctx.reply("❌ صيغة الأمر: سحب <UID> <المبلغ>");

        const target_uid = parseInt(parts[1]);
        const amount = parseInt(parts[2]);
        if (isNaN(target_uid) || isNaN(amount)) return ctx.reply("❌ يجب أن يكون UID والمبلغ أرقاماً صحيحة");

        const target_user = await _get_user(target_uid);
        const old_gold = target_user.gold || 0;
        const new_gold = Math.max(0, old_gold - amount);

        await update_user_gold(target_uid, -amount);

        const target_name = target_user.name || target_uid;
        const target_username = target_user.username ? `@${target_user.username}` : target_uid;

        return ctx.reply(`💰 سحب ${amount} ذهب من ${target_name} / ${target_username}\nالرصيد الجديد: ${new_gold}`);
    }

    // ======================
    // قائمة التصنيف
    // ======================
    if (text.startsWith("تصنيف")) {
        const all_users = await _get_all_users_list();

        const richest = all_users.sort((a,b) => (b.gold||0) - (a.gold||0)).slice(0,5);
        const active = all_users.sort((a,b) => (b.total_messages||0) - (a.total_messages||0)).slice(0,5);

        let report = "╔═════════════════╗\n   قائمة التصنيف\n╚═════════════════╝\n\n";

        report += "أغنى 5 أشخاص بالبوت:\n\n";
        richest.forEach((u,i) => {
            const name = u.name || "بدون اسم";
            report += `${i+1}- ${name} / UID: ${u.uid} / ذهب: ${u.gold||0}\n`;
        });

        report += "\n━━━━━━━━━━━━━━━\nأكثر 5 أشخاص تفاعلاً:\n\n";
        active.forEach((u,i) => {
            const name = u.name || "بدون اسم";
            report += `${i+1}- ${name} / UID: ${u.uid} / رسائل: ${u.total_messages||0}\n`;
        });

        report += "━━━━━━━━━━━━━━━";
        return ctx.reply(report);
    }
}

// ======================
// دالة مساعدة للحصول على كل المستخدمين
// ======================
async function _get_all_users_list() {
    return users.find({}).toArray();
}

module.exports = { handle };
