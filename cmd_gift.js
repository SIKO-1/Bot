// ملف: cmd_gift.js
const COMMANDS = ["هدية"];
const DAY = 24 * 60 * 60 * 1000; // 24 ساعة بالميلي ثانية
const db_manager = require("./db_manager"); // تأكد من مسار الملف

// =========================
// التحقق إذا المستخدم يقدر ياخذ هديته
// =========================
async function canTakeGift(uid) {
    const user = await db_manager.getUser(uid);
    const lastGift = user.last_gift_time || 0;
    return Date.now() - lastGift >= DAY;
}

// =========================
// استلام الهدية
// =========================
async function takeGift(uid, amount = 100) {
    if (!(await canTakeGift(uid))) return null;

    await db_manager.updateUserGold(uid, amount);
    await db_manager.users.updateOne({ uid }, { $set: { last_gift_time: Date.now() } });
    return await db_manager.getUserGold(uid);
}

// =========================
// التعامل مع الأمر
// =========================
async function handle(bot, msg) {
    if (!msg.text || !COMMANDS.includes(msg.text.trim())) return;

    const uid = msg.from.id;

    if (await canTakeGift(uid)) {
        const amount = await takeGift(uid);
        bot.sendMessage(msg.chat.id, `🎁 لقد استلمت هديتك اليومية!\n+${amount} ذهب 💰`);
        return;
    }

    // =========================
    // حساب الوقت المتبقي
    // =========================
    const user = await db_manager.getUser(uid);
    const lastGift = user.last_gift_time || 0;
    let remaining = DAY - (Date.now() - lastGift);
    if (remaining < 0) remaining = 0;

    const hours = Math.floor(remaining / (1000 * 60 * 60));
    const minutes = Math.floor((remaining % (1000 * 60 * 60)) / (1000 * 60));
    // const seconds = Math.floor((remaining % (1000 * 60)) / 1000); // لو حبيت تضيف الثواني

    bot.sendMessage(
        msg.chat.id,
        `⏳ انتظر قبل استلام هديتك القادمة:\n ${hours} ساعة و ${minutes} دقيقة`
        // + ` و ${seconds} ثانية` // لو تريد الثواني
    );
}

module.exports = { handle, canTakeGift, takeGift };
