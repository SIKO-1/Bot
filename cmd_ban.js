// cmd_ban.js
const db = require('./db_manager');

const DEV_IDS = [5860391324, 7076215547, 7855813063]

const COMMANDS_BAN = ["حظر"];
const COMMANDS_PARDON = ["عفو"];
const COMMANDS_LIST = ["قائمة الحظر", "الحظر"];

function handle(bot, ctx) {
    const uid = ctx.from.id;
    const user_name = ctx.from.first_name;
    const text = ctx.message?.text?.trim();

    if (!text) return;

    // ===== حظر المستخدم =====
    if (COMMANDS_BAN.some(cmd => text.startsWith(cmd))) {
        if (uid !== DEV_ID) return;
        if (!ctx.message.reply_to_message) {
            ctx.reply("⚠️ الرجاء الرد على رسالة الشخص الذي تريد حظره!");
            return;
        }
        const target_id = ctx.message.reply_to_message.from.id;
        db.ban_user(target_id);
        ctx.reply(`👑 ${user_name} أمر الإمبراطور: تم حظر الشخص بنجاح!`);
        return;
    }

    // ===== العفو عن المستخدم =====
    if (COMMANDS_PARDON.some(cmd => text.startsWith(cmd))) {
        if (uid !== DEV_ID) return;
        if (!ctx.message.reply_to_message) {
            ctx.reply("⚠️ الرجاء الرد على رسالة الشخص الذي تريد العفو عنه!");
            return;
        }
        const target_id = ctx.message.reply_to_message.from.id;
        db.unban_user(target_id);
        ctx.reply(`👑 ${user_name} أمر الإمبراطور: تم العفو عن الشخص!`);

        // إرسال رسالة للعفو عنه
        try {
            bot.telegram.sendMessage(target_id, "👑 تم العفو عنك بأمر الإمبراطور! اشكر الإمبراطور 🌟");
        } catch {}
        return;
    }

    // ===== عرض قائمة الحظر =====
    if (COMMANDS_LIST.includes(text)) {
        if (uid !== DEV_ID) {
            ctx.reply("❌ هذا الأمر للمطور فقط!");
            return;
        }
        const banned_users = db.get_banned_users ? db.get_banned_users() : [];
        if (!banned_users.length) {
            ctx.reply("📜 لا يوجد أي شخص محظور حالياً.");
            return;
        }
        let text_list = "📜 قائمة المحظورين:\n\n";
        banned_users.forEach(u => text_list += `👤 ID: ${u}\n`);
        ctx.reply(text_list);
        return;
    }

    // ===== الصمت لأي شخص محظور =====
    if (db.is_user_banned(uid)) {
        try {
            ctx.deleteMessage(ctx.message.message_id).catch(() => {});
        } catch {}
        return;
    }
}

module.exports = { handle };
