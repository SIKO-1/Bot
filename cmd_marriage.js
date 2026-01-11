// ملف: cmd_marriage.js
const COMMANDS = ["زوجني", "طلقني", "قائمة المتزوجين"];
const db_manager = require("./db_manager");

// ======= إعداد الزواج =======
let marriage_enabled = true;

async function isAlreadyMarried(uid) {
    const marriage = await db_manager.users.findOne({
        $or: [{ husband_uid: uid }, { wife_uid: uid }]
    });
    return marriage !== null;
}

async function getMarriage(uid) {
    return await db_manager.users.findOne({
        $or: [{ husband_uid: uid }, { wife_uid: uid }]
    });
}

// ======= أمر زوجني =======
async function marryUser(bot, message, target_identifier) {
    const user = await db_manager.getUser(message.from.id);

    if (await isAlreadyMarried(user.uid)) {
        bot.replyTo(message, "⚠️ أنت متزوج بالفعل!");
        return;
    }

    let target_user = null;

    if (!target_identifier) {
        // اختيار عشوائي من المستخدمين الموجودين في DB
        const allUsers = await db_manager.users.find({ uid: { $ne: user.uid } }).toArray();
        target_user = allUsers[Math.floor(Math.random() * allUsers.length)];
    } else if (target_identifier.startsWith("@")) {
        target_user = await db_manager.users.findOne({ username: target_identifier.slice(1) });
    } else {
        try {
            const target_uid = parseInt(target_identifier);
            target_user = await db_manager.getUser(target_uid);
        } catch {
            bot.replyTo(message, "⚠️ الرجاء كتابة UID صالح أو @username");
            return;
        }
    }

    if (!target_user) {
        bot.replyTo(message, "⚠️ لم يتم العثور على المستخدم المطلوب.");
        return;
    }

    if (await isAlreadyMarried(target_user.uid)) {
        bot.replyTo(message, "⚠️ هذا الشخص متزوج بالفعل!");
        return;
    }

    // تسجيل الزواج
    await db_manager.users.insertOne({
        husband_uid: user.uid,
        wife_uid: target_user.uid,
        married_at: Date.now()
    });

    const text = `💍 تم الزواج بنجاح بين:
• ${user.uid} (${user.username || "بدون اسم"}) ❤️
• ${target_user.uid} (${target_user.username || "بدون اسم"})`;

    // إرسال صورة ميمز ثابتة مع النص (يمكن تغيير الرابط حسب اختيارك)
    const meme_url = "https://i.imgur.com/9bX5YUw.jpg"; // مثال لميمز زواج
    bot.sendPhoto(message.chat.id, meme_url, { caption: text });
}

// ======= أمر طلقني =======
async function divorce(bot, message) {
    const user = await db_manager.getUser(message.from.id);
    const marriage = await getMarriage(user.uid);
    if (!marriage) {
        bot.replyTo(message, "⚠️ أنت غير متزوج حالياً!");
        return;
    }

    await db_manager.users.deleteOne({ _id: marriage._id });
    bot.replyTo(message, "💔 تم الطلاق بنجاح!");
}

// ======= قائمة المتزوجين =======
async function listMarried(bot, message) {
    const all_marriages = await db_manager.users.find({ husband_uid: { $exists: true } }).toArray();
    if (!all_marriages.length) {
        bot.replyTo(message, "لا يوجد متزوجين حالياً.");
        return;
    }

    let text = "💑 قائمة المتزوجين:\n";
    for (const m of all_marriages) {
        const husband = await db_manager.getUser(m.husband_uid);
        const wife = await db_manager.getUser(m.wife_uid);
        text += `• ${husband.uid} (${husband.username || "بدون اسم"}) ❤️ ${wife.uid} (${wife.username || "بدون اسم"})\n`;
    }

    bot.sendMessage(message.chat.id, text);
}

// ======= Handler =======
async function handle(bot, message) {
    if (!marriage_enabled) return;

    const text = message.text?.trim();
    if (!text) return;

    if (text.startsWith("زوجني")) {
        const parts = text.split(/\s+/);
        const target_identifier = parts[1] || null; // إذا ما ذكر، يكون عشوائي
        await marryUser(bot, message, target_identifier);
    } else if (text === "طلقني") {
        await divorce(bot, message);
    } else if (text === "قائمة المتزوجين") {
        await listMarried(bot, message);
    }
}

module.exports = { handle };
