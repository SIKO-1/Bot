// ملف: cmd_games_buttons.js
const COMMANDS = ["الالعاب", "العاب", "لعبات"];

// قائمة كل الألعاب + وصفها
const GAMES = {
    "نرد": "لعبة رمي النرد الإمبراطوري",
    "روليت": "لعبة الروليت الإمبراطوري",
    "المختلف": "لعبة المختلف",
    "امثله": "لعبة الأمثلة",
    "العكس": "لعبة عكس الكلمة",
    "حزوره": "لعبة الحزورة",
    "معاني": "لعبة المعاني",
    "بات": "لعبة البات",
    "خمن": "لعبة التخمين",
    "ترتيب": "لعبة ترتيب الحروف",
    "سمايلات": "لعبة السمايلات",
    "اسئله": "أسئلة منوعة",
    "اسالني": "أسئلة عامة متجددة",
    "لغز": "ألغاز الذكاء المتجددة",
    "رياضيات": "مسائل رياضية",
    "انكليزي": "معاني الكلمات",
    "كت": "أسئلة ترفيهية",
    "كت تويت": "أسئلة ترفيهية",
    "لو خيروك": "لعبة لو خيروك",
    "صراحه": "لعبة الصراحة",
    "اعلام": "لعبة اعلام الدول",
    "مقالات": "لعبة المقالات",
    "عواصم": "لعبة عواصم الدول",
    "كلمات": "لعبة كتابة الكلمات",
    "الحظ": "لعبة الحظ الشفافة",
    "حظي": "لعبة ربح أو خسارة",
    "اغاني": "لعبة اسم الفنان",
    "تحدي": "لعبة صراحة مع تاك عشوائي",
    "XO": "لعبة XO الشفافة",
    "رقم": "لعبة أرقام عشوائية",
    "المليون": "لعبة من سيربح المليون",
    "نشط عقلك": "لعبة أسئلة منوعة"
};

// ======================
// عرض الألعاب + أزرار Inline
// ======================
function handle(bot, msg) {
    if (!msg.text) return;
    if (!COMMANDS.includes(msg.text.trim())) return;

    const userName = msg.from.first_name || "المستخدم";

    const text = `
╔═════════════════╗
      الألعاب الإمبراطورية
╚═════════════════╝

مرحباً بك يا ${userName} 👑
━━━━━━━━━━━━━━━
اضغط على أي لعبة لمعرفة معلوماتها:
`;

    // تجهيز الأزرار كل 2 أزرار في صف
    const buttons = [];
    const gameNames = Object.keys(GAMES);
    for (let i = 0; i < gameNames.length; i += 2) {
        const row = [];
        row.push({ text: gameNames[i], callback_data: `game_${gameNames[i]}` });
        if (gameNames[i + 1]) {
            row.push({ text: gameNames[i + 1], callback_data: `game_${gameNames[i + 1]}` });
        }
        buttons.push(row);
    }

    bot.sendMessage(msg.chat.id, text, {
        reply_markup: { inline_keyboard: buttons }
    });
}

// ======================
// الرد على الضغط على زر اللعبة
// ======================
function registerCallbacks(bot) {
    bot.on('callback_query', async (call) => {
        if (!call.data.startsWith("game_")) return;

        const gameName = call.data.replace("game_", "");
        const description = GAMES[gameName] || "❌ معلومات غير موجودة لهذه اللعبة";

        await bot.answerCallbackQuery(call.id);
        bot.sendMessage(call.message.chat.id, `🎮 ${gameName}:\n${description}`);
    });
}

module.exports = { handle, registerCallbacks };
