// ملف: cmd_daily_task.js

const COMMANDS = ["مهمتي", "انجزت"];

function handle(bot, ctx, db) {
    if (!ctx.message || !ctx.message.text) return;

    const uid = ctx.from.id;
    const text = ctx.message.text.trim();

    // ======================
    // عرض المهمة
    // ======================
    if (text === "مهمتي") {
        const task = db.get_daily_task(uid);

        // لا توجد مهمة + وقت انتظار
        if (!task) {
            const remaining = db.time_left_for_task(uid);
            if (remaining) {
                ctx.reply(
                    "⏳ لا يمكنك أخذ مهمة الآن\n\n" +
                    `🕒 الوقت المتبقي:\n${remaining}\n\n` +
                    "اصبر… صندوق الحظ يحب الصابرين 🎁"
                );
            } else {
                ctx.reply("❌ لا توجد مهمة حالياً.");
            }
            return;
        }

        // عرض المهمة
        ctx.reply(
            "🎯 مهمتك لليوم:\n" +
            `${task.desc}\n\n` +
            "✍️ بعد إنجازها اكتب:\n" +
            "👉 انجزت"
        );
        return;
    }

    // ======================
    // إنجاز المهمة يدويًا
    // ======================
    if (text === "انجزت") {
        const task = db.get_daily_task(uid);

        if (!task) {
            ctx.reply("❌ ما عندك مهمة اليوم.");
            return;
        }

        const completed = db.complete_mission(uid, "manual");

        if (!completed) {
            ctx.reply("⚠️ مهمتك منجزة مسبقًا أو غير صالحة.");
            return;
        }

        db.add_to_inventory(uid, "🎁 صندوق الحظ النادر");

        ctx.reply(
            "✅ تم إنجاز مهمتك اليومية بنجاح!\n\n" +
            "🎁 حصلت على صندوق الحظ النادر\n" +
            "📦 اكتب: مخزوني لعرضه"
        );
        return;
    }
}

// ======================
// تُستدعى من الألعاب
// ======================
function check_task_completion(bot, ctx, db, mission_type) {
    const uid = ctx.from.id;

    const completed = db.complete_mission(uid, mission_type);
    if (!completed) return;

    db.add_to_inventory(uid, "🎁 صندوق الحظ النادر");

    ctx.reply(
        "✅ تم إكمال مهمتك اليومية!\n\n" +
        "🎁 صندوق الحظ النادر أُضيف لمخزونك\n" +
        "📦 اكتب: مخزوني"
    );
}

module.exports = {
    handle,
    check_task_completion
};
