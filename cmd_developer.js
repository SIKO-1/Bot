// ملف: cmd_developer.js
const COMMANDS = ["المطور"];
const DEV_ID = 5860391324; // آيدي المطور
const USERNAME = "@Om_rtl"; // معرفك
const DEFAULT_RANK = "المطور الأساسي";
const BIO = "وَاصْبِرْ فَإِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ";

// اقتباس فلسفي مجنون
const QUOTE = '⌁︙"المطور لا يكتب أوامر…\nهو يخلق قوانين، ثم يراقب الفوضى وهي تطيع."';

async function handle(bot, ctx, db) {
    const text = ctx.message.text?.trim();
    const uid = ctx.from.id;

    if (!text || !COMMANDS.includes(text)) return;

    if (uid !== DEV_ID) {
        ctx.reply("❌ هذا الأمر مخصص للمطور فقط");
        return;
    }

    // محاولة جلب الرتبة من db_manager
    let rank = DEFAULT_RANK;
    try {
        const db_rank = await db.getUserRank(DEV_ID);
        if (db_rank !== null && db_rank !== undefined) rank = db_rank;
    } catch (err) {
        console.log("⚠️ خطأ جلب الرتبة من DB:", err.message);
    }

    // تجهيز النص
    const replyText = `${QUOTE}\n\n` +
        `⌁︙ايدي الـمُطَور ↫ ${DEV_ID}\n` +
        `⌁︙معرف الـمُطَور ↫ ${USERNAME}\n` +
        `⌁︙حساب الـمُطَور ↫ مُميز\n` +
        `⌁︙رتبة الـمُطَور ↫ ${rank}\n` +
        `⌁︙البـايـــو ↫ ${BIO}`;

    try {
        const photos = await bot.telegram.getUserProfilePhotos(DEV_ID, { limit: 1 });
        if (photos.total_count > 0) {
            const file_id = photos.photos[0][photos.photos[0].length - 1].file_id;
            await bot.telegram.sendPhoto(ctx.chat.id, file_id, { caption: replyText });
            return;
        }
    } catch (err) {
        console.log("⚠️ خطأ جلب صورة البروفايل:", err.message);
    }

    // إذا ماكو صورة
    ctx.reply(replyText);
}

module.exports = { handle };
