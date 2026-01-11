// ملف: cmd_level.js
const COMMANDS = ["مستوى", "لفلي", "lv"];
const db_manager = require("./db_manager");

// دالة لحساب المستوى بناءً على الذهب أو أي عوامل مستقبلية
function calculateLevel(gold) {
    // قاعدة: كل مستوى يحتاج ذهب أكثر من السابق (تصاعدي)
    // المستوى 0-1 = 50 ذهب، ثم المستوى التالي يزيد 20% عن السابق
    let level = 0;
    let required = 50;

    while (gold >= required) {
        gold -= required;
        level++;
        required = Math.floor(required * 1.2); // كل مستوى يصعب أكثر
    }

    return { level, remaining: required - gold };
}

// ألقاب حسب المستوى
function getTitle(level) {
    if (level < 10) return "مبتدئ الإمبراطورية";
    if (level < 50) return "محارب الظل";
    if (level < 100) return "سيد الساحة";
    return "أسطورة كيرا";
}

async function handle(bot, msg) {
    if (!msg.text) return;
    if (!COMMANDS.includes(msg.text.trim())) return;

    const uid = msg.from.id;
    const gold = await db_manager.getUserGold(uid);

    const { level, remaining } = calculateLevel(gold);
    const title = getTitle(level);

    // حفظ المستوى الحالي في قاعدة البيانات
    await db_manager.setUserRank(uid, level);

    const text = `
╔═════════════════╗
      المستوى
╚═════════════════╝

↫ مستواك ↫ ${level}
↫ لقبك ↫ ${title}
↫ رصيدك ↫ ${gold} ذهب
↫ للمستوى القادم ↫ ${remaining} ذهب
`;

    bot.sendMessage(msg.chat.id, text);
}

module.exports = { handle };
