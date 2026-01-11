// ملف: cmd_beauty_iraqi.js
const crypto = require("crypto");

const COMMANDS = ["جمالي"];

// رموز حسب النسبة
const EMOJIS = [
    { low: 0, high: 20, emoji: "💀❌" },
    { low: 21, high: 40, emoji: "😅🙃" },
    { low: 41, high: 60, emoji: "🙂✨" },
    { low: 61, high: 80, emoji: "😍🌟" },
    { low: 81, high: 99, emoji: "🤩👑" },
    { low: 100, high: 100, emoji: "👑🌹🔥" }
];

// أوصاف حسب النسبة – لهجة عراقية
const DESCRIPTIONS = [
    {
        low: 0,
        high: 20,
        texts: [
            "ههه، الظل يمشي أحسن منك 😅",
            "الجمال مو كلشي، روحك أهم 🌫️"
        ]
    },
    {
        low: 21,
        high: 40,
        texts: [
            "إي زين شوية، بس مو كلش 😉",
            "ابتسامتك خفيفة، تكفي تفرّح 😏"
        ]
    },
    {
        low: 41,
        high: 60,
        texts: [
            "زين، وجهك حلو، وقلبك أحلى ❤️",
            "توازن جميل بين الزين والوسط 🌌"
        ]
    },
    {
        low: 61,
        high: 80,
        texts: [
            "واو، تلمع مثل الشمس ☀️",
            "إشراقتك تخلي الكل يدورلك 👀"
        ]
    },
    {
        low: 81,
        high: 99,
        texts: [
            "أنت وجه ساحر والله 😍",
            "الجمال يمشي وياك وين ما تروح ✨"
        ]
    },
    {
        low: 100,
        high: 100,
        texts: [
            "👑 ملك/ة جمال الكون! محد يضاهيك",
            "🔥 الجمال المطلق… كلشي قدامك صغير"
        ]
    }
];

// يعطي نسبة ثابتة تقريبًا لكل شخص
function deterministicScore(uid) {
    const hash = crypto
        .createHash("sha256")
        .update(uid.toString())
        .digest("hex");

    const num = parseInt(hash.substring(0, 8), 16);
    return (num % 100) + 1;
}

function getEmoji(score) {
    const found = EMOJIS.find(e => score >= e.low && score <= e.high);
    return found ? found.emoji : "❔";
}

function getDescription(score, uid) {
    const found = DESCRIPTIONS.find(d => score >= d.low && score <= d.high);
    if (!found) return "🤔 نسبة غريبة";

    const index = (uid + score) % found.texts.length;
    return found.texts[index];
}

async function handle(bot, ctx) {
    if (!ctx.message || !ctx.message.text) return;

    const text = ctx.message.text.trim();
    if (!COMMANDS.includes(text)) return;

    const userId = ctx.from.id;
    const userName = ctx.from.first_name || "مستخدم";

    const score = deterministicScore(userId);
    const emoji = getEmoji(score);
    const description = getDescription(score, userId);

    try {
        const photos = await bot.telegram.getUserProfilePhotos(userId, 0, 1);

        if (photos.total_count > 0) {
            const fileId = photos.photos[0][photos.photos[0].length - 1].file_id;

            await ctx.replyWithPhoto(fileId, {
                caption: `✨ جمال ${userName}: ${score}/100 ${emoji}\n${description}`
            });
        } else {
            await ctx.reply(
                `✨ جمال ${userName}: ${score}/100 ${emoji}\n${description}\n⚠️ ماكو صورة بالبروفايل`
            );
        }
    } catch (err) {
        await ctx.reply("❌ صار خطأ وأنا أطلع النتيجة، بس الجمال ثابت 😌");
    }
}

module.exports = { handle };
