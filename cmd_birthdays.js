// ملف: cmd_birthdays.js
const fs = require("fs");
const path = require("path");
const { Telegraf } = require("telegraf");
const db = require("./db_manager");

const COMMANDS = [
    "اضف عيد",
    "مسح عيد",
    "عيد ميلاد",
    "قائمه الاعياد",
    "تفعيل عيد ميلاد",
    "تعطيل عيد ميلاد",
    "زواج"
];

const CHECK_INTERVAL = 5 * 60 * 1000; // 5 دقائق

// =====================
// أوامر المستخدم
// =====================
async function handle(bot, ctx) {
    if (!ctx.message || !ctx.message.text) return;

    const text = ctx.message.text.trim();
    const uid = ctx.from.id;

    try {
        // ===== إضافة عيد =====
        if (text.startsWith("اضف عيد")) {
            const parts = text.split(" ");
            if (parts.length < 5) {
                return ctx.reply("❌ الصيغة: اضف عيد <ID> <اليوم> <الشهر> [السنة]");
            }

            const targetUid = Number(parts[2]);
            const day = Number(parts[3]);
            const month = Number(parts[4]);
            const year = parts[5] ? Number(parts[5]) : null;

            const res = await db.add_birthday(targetUid, day, month, year);
            if (res.ok) {
                ctx.reply(`✅ تم إضافة عيد الميلاد\nUID: ${targetUid}\n📅 ${day}/${month}/${year ?? "؟"}`);
            } else {
                ctx.reply(res.error);
            }
        }

        // ===== مسح عيد =====
        else if (text.startsWith("مسح عيد")) {
            const parts = text.split(" ");
            if (parts.length < 3) {
                return ctx.reply("❌ الصيغة: مسح عيد <ID>");
            }

            await db.remove_birthday(Number(parts[2]));
            ctx.reply("✅ تم مسح عيد الميلاد");
        }

        // ===== عرض عيد =====
        else if (text.startsWith("عيد ميلاد")) {
            const parts = text.split(" ");
            if (parts.length < 3) {
                return ctx.reply("❌ الصيغة: عيد ميلاد <ID>");
            }

            const bd = await db.get_birthday(Number(parts[2]));
            if (!bd) return ctx.reply("⚠️ ما مسجل عيد ميلاد");

            ctx.reply(
                `🎂 عيد الميلاد:\n📅 ${bd.day}/${bd.month}/${bd.year ?? "؟"}`
            );
        }

        // ===== قائمة =====
        else if (text === "قائمه الاعياد") {
            const list = await db.list_birthdays();
            if (!list.length) return ctx.reply("⚠️ ماكو أعياد مسجلة");

            let msg = "🎉 قائمة الأعياد:\n\n";
            for (const b of list) {
                msg += `• ${b.uid} → ${b.birthday.day}/${b.birthday.month}/${b.birthday.year ?? "؟"}\n`;
            }
            ctx.reply(msg);
        }

        // ===== تفعيل / تعطيل =====
        else if (text === "تفعيل عيد ميلاد") {
            await db.enable_birthday_auto(uid);
            ctx.reply("✅ تم التفعيل");
        }

        else if (text === "تعطيل عيد ميلاد") {
            await db.disable_birthday_auto(uid);
            ctx.reply("🚫 تم التعطيل");
        }

        // =====================
        // 💍 زواج عشوائي
        // =====================
        else if (text === "زواج") {
            if (!ctx.message.reply_to_message) {
                return ctx.reply("💍 رد على رسالة الشخص حتى أزوجكم 😏");
            }

            const user1 = ctx.from;
            const user2 = ctx.message.reply_to_message.from;

            const captions = [
                `💍 مبروك الزواج!\n${user1.first_name} ❤️ ${user2.first_name}\nالله بالخير 👰🤵`,
                `😂 تم عقد القِران!\n${user1.first_name} × ${user2.first_name}\nزواج ميمز رسمي`,
                `👑 زوجين VIP\n${user1.first_name} 🤍 ${user2.first_name}`
            ];

            const memesDir = path.join(__dirname, "assets", "marriage");
            const images = fs.readdirSync(memesDir);
            const randomImg = images[Math.floor(Math.random() * images.length)];
            const caption = captions[Math.floor(Math.random() * captions.length)];

            await ctx.replyWithPhoto(
                { source: path.join(memesDir, randomImg) },
                { caption }
            );
        }

    } catch (err) {
        ctx.reply("❌ صار خطأ غير متوقع");
    }
}

// =====================
// 🎂 جدولة التهاني
// =====================
function startBirthdayScheduler(bot) {
    setInterval(async () => {
        const today = new Date();
        const list = await db.list_birthdays();

        for (const b of list) {
            const bd = b.birthday;
            if (bd.day === today.getDate() && bd.month === today.getMonth() + 1) {

                if (!(await db.is_birthday_auto_enabled(b.uid))) continue;

                try {
                    const user = await bot.telegram.getChat(b.uid);
                    const msg = `🎉 كل عام وأنت بخير ${user.first_name}!\n🎂 عيد ميلاد سعيد`;

                    const imgPath = path.join(__dirname, "assets", "birthday.jpg");

                    if (fs.existsSync(imgPath)) {
                        await bot.telegram.sendPhoto(b.uid, { source: imgPath }, { caption: msg });
                    } else {
                        await bot.telegram.sendMessage(b.uid, msg);
                    }
                } catch {}
            }
        }
    }, CHECK_INTERVAL);
}

module.exports = {
    handle,
    startBirthdayScheduler
};
