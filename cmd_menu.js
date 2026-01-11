const { get_user_gold, _get_user } = require('./db_manager');
const { Markup } = require('telegraf');

// جمل عشوائية للهوية
const ID_QUOTES = [
    "مو كل اسم ينكتب… بعضهم ينحفر.",
    "الحضور ما يحتاج تعريف.",
    "الهيبة أسلوب، مو ضجيج.",
    "مكانك ثابت حتى لو تغيّر المكان.",
    "الصمت أحيانًا أفخم من الكلام.",
    "مو رقم… هو توقيع.",
    "الاسم بسيط، التأثير ثقيل.",
    "الهيبة ما تنشرح، تنفهم.",
    "مو نسخة، أصل.",
    "بعض الناس ما يحتاجون لقب."
];

const MENU_TEXT = `
╔═════════════════╗
   الأوامر الإمبراطورية
╚═════════════════╝

مرحباً بك في بوت كيرا
يا {name}

━━━━━━━━━━━━━━━

الأقسام :

• الألعاب
• المتجر
• البنك
• تسلية 
• شؤون الإدارة

━━━━━━━━━━━━━━━

شؤون الإدارة :
• إدارة

━━━━━━━━━━━━━━━
لعرض هويتك أرسل :
〔 ا 〕 أو 〔 ايدي 〕

━━━━━━━━━━━━━━━
الدنيا مو عادلة… بس الهيبة تختار أصحابها.
`;

function get_user_rank_in_bot(uid) {
    const user = _get_user(uid);
    const rank_val = user.rank || 0;
    if (rank_val === 0) return "عضو";
    if (rank_val === 1) return "مشرف";
    if (rank_val >= 2) return "مالك / مطور";
    return "عضو";
}

function handle(bot, ctx) {
    const DEV_IDS = process.env.DEV_IDS ? process.env.DEV_IDS.split(',').map(id => id.trim()) : [];
    const text = ctx.message.text.trim();

    // ===== قائمة الأوامر =====
    if (["اوامر", "الأوامر"].includes(text)) {
        ctx.reply(MENU_TEXT.replace("{name}", ctx.from.first_name));
        return;
    }

    // ===== أمر الايدي =====
    if (["ا", "ايدي"].includes(text)) {
        let user = ctx.from;

        // إذا المطور رد على شخص ثاني
        if (ctx.message.reply_to_message && DEV_IDS.includes(ctx.from.id)) {
            user = ctx.message.reply_to_message.from;
        }

        const uid = user.id;
        const quote = ID_QUOTES[Math.floor(Math.random() * ID_QUOTES.length)];
        const gold = get_user_gold(uid);
        const username = user.username ? `@${user.username}` : `${uid}`;
        const bio = user.bio || "";
        const rank = get_user_rank_in_bot(uid);
        const accountType = user.is_premium ? "حساب مميز" : "حساب عادي";

        const text_id = `
↫ ${quote}

⌁︙ايديڪ↫ ${uid}
⌁︙معرفڪ↫ ${username}
⌁︙حسابڪ↫ ${accountType}
⌁︙رتبتڪ بالبـوت↫ ${rank}
⌁︙فلوسڪ↫ ${gold} ذهب
⌁︙البـايـــو↫ ${bio}
`;

        ctx.reply(text_id);
    }
}

module.exports = { handle };
