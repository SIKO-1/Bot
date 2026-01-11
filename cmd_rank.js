// ملف: cmd_rank.js
const db_manager = require('./db_manager');

// ======================
// إعداد المطورين
// ======================
const DEV_IDS = [5860391324, 7076215547, 7855813063]; // أضف أي ايدي مطورين آخرين هنا
const MAX_RANK = 25;

const RANKS = {
    0: ["بدون رتبة", 0],
    1: ["جندي", 500],
    2: ["محارب", 1200],
    3: ["فارس", 2500],
    4: ["قائد", 5000],
    5: ["نخبة", 9000],
    6: ["كابتن", 15000],
    7: ["جنرال", 22000],
    8: ["مارشال", 30000],
    9: ["بارون", 40000],
    10: ["كونت", 55000],
    11: ["دوق", 75000],
    12: ["أمير", 100000],
    13: ["ولي العهد", 140000],
    14: ["لورد", 190000],
    15: ["لورد أعلى", 250000],
    16: ["نبيل الإمبراطورية", 320000],
    17: ["حاكم", 400000],
    18: ["حاكم أعلى", 500000],
    19: ["ملك", 650000],
    20: ["ملك عظيم", 850000],
    21: ["إمبراطور صغير", 1100000],
    22: ["إمبراطور", 1500000],
    23: ["إمبراطور أعظم", 2000000],
    24: ["ظل الإمبراطور", 3000000],
    25: ["👑 الإمبراطور المطلق 👑", null] // لا تُشترى
};

// ======================
// الهاندلر
// ======================
function handle(bot, message) {
    if (!message.text) return;
    const text = message.text.trim();
    const uid = message.from_user.id;

    // ======= عرض قائمة الرتب =======
    if (text === "رتب") {
        let msg = "🏷️ قائمة الرتب:\n\n";
        for (let i = 1; i <= MAX_RANK; i++) {
            const [name, price] = RANKS[i];
            if (price === null) {
                msg += `${i}. ${name} — ❌ خاصة\n`;
            } else {
                msg += `${i}. ${name} — 💰 ${price}\n`;
            }
        }
        bot.sendMessage(message.chat.id, msg);
        return;
    }

    // ======= عرض رتبتك =======
    if (text === "رتبتي") {
        const rank = db_manager.get_user_rank(uid);
        const [name] = RANKS[rank] || ["بدون رتبة"];
        bot.sendMessage(message.chat.id, `🎖️ رتبتك الحالية:\n${name} (#${rank})`);
        return;
    }

    // ======= شراء رتبة =======
    if (text.startsWith("رتبة")) {
        const parts = text.split(" ");
        const target = parseInt(parts[1]);
        if (isNaN(target)) {
            bot.sendMessage(message.chat.id, "❌ اكتب: رتبة رقم");
            return;
        }

        const current = db_manager.get_user_rank(uid);
        if (target !== current + 1) {
            bot.sendMessage(message.chat.id, "❌ لازم تشتري الرتب بالترتيب");
            return;
        }

        const [name, price] = RANKS[target] || [null, null];
        if (price === null) {
            bot.sendMessage(message.chat.id, "🚫 هذه الرتبة لا تُشترى");
            return;
        }

        const gold = db_manager.get_user_gold(uid);
        if (gold < price) {
            bot.sendMessage(message.chat.id, "💸 ذهبك غير كافي");
            return;
        }

        db_manager.update_user_gold(uid, -price);
        db_manager.set_user_rank(uid, target);
        bot.sendMessage(message.chat.id, `✅ تمت الترقية!\n🎖️ رتبتك الجديدة: ${name}`);
        return;
    }

    // ======= ترقية بالقوة (للمطورين فقط) =======
    if (text.startsWith("ترقية")) {
        if (!DEV_IDS.includes(uid)) return;

        const parts = text.split(" ");
        if (parts.length < 3) {
            bot.sendMessage(message.chat.id, "❌ الصيغة: ترقية ايدي الرتبة");
            return;
        }

        const target_uid = parseInt(parts[1]);
        const target_rank = parseInt(parts[2]);

        if (isNaN(target_uid) || isNaN(target_rank)) {
            bot.sendMessage(message.chat.id, "❌ ايدي أو رتبة غير صحيحة");
            return;
        }

        if (!(target_rank in RANKS)) {
            bot.sendMessage(message.chat.id, "❌ رتبة غير موجودة");
            return;
        }

        db_manager.set_user_rank(target_uid, target_rank);
        const [name] = RANKS[target_rank];
        bot.sendMessage(message.chat.id, `👑 تمت الترقية بالقوة الإمبراطورية!\nالرتبة الجديدة: ${name}`);
        return;
    }
}

module.exports = { handle };
