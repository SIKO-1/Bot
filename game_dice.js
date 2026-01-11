// game_dice.js
const db = require('./db_manager');

const COMMAND = "نرد";
const MISSION_TYPE = "dice";       // نوع المهمة في db_manager
const REWARD_ITEM = "🎁 صندوق الحظ النادر";

async function handle(bot, ctx) {
    if (ctx.message.text !== COMMAND) return;

    const uid = ctx.from.id;
    const inventory = await db.get_inventory(uid);

    // رسالة ترحيب مؤقتة
    await ctx.reply("🎲 جاري رمي نرد الإمبراطورية...\n⚔️ ركّز، فالحظ لا يبتسم مرتين.");

    try {
        // إرسال نرد Telegram
        const diceMsg = await ctx.sendDice();
        const value = diceMsg.dice.value;

        // تأثير درامي
        await new Promise(r => setTimeout(r, 3500));

        let resultText = "";
        let prizeOrPenalty = 0;

        if (value >= 5) {
            // فوز إمبراطوري
            prizeOrPenalty = 200;
            if (inventory.includes("سيف الإمبراطور 🔱")) prizeOrPenalty = Math.floor(prizeOrPenalty * 1.2);
            if (inventory.includes("قفاز القوة")) prizeOrPenalty = Math.floor(prizeOrPenalty * 1.25);
            if (inventory.includes("خاتم الحظ 💍") && Math.random() < 0.1) prizeOrPenalty += 50;

            const newGold = await db.update_user_gold(uid, prizeOrPenalty);
            resultText = `
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ فـوز إمـبـراطـوري ⌯
┗━━━━━━━ ● ━━━━━━━┛

🔥 الحظ يبتسم لك : [ ${value} ]
💰 الجائزة : +${prizeOrPenalty} ذهب
✨ رصيدك الحالي : ${newGold} ذهب
            `;
        } else if (value >= 3) {
            // حظ متوسط
            prizeOrPenalty = 50;
            if (inventory.includes("سيف الإمبراطور 🔱")) prizeOrPenalty = Math.floor(prizeOrPenalty * 1.2);
            if (inventory.includes("قفاز القوة")) prizeOrPenalty = Math.floor(prizeOrPenalty * 1.25);

            const newGold = await db.update_user_gold(uid, prizeOrPenalty);
            resultText = `
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ حظ متوسط ⌯
┗━━━━━━━ ● ━━━━━━━┛

🔥 الحظ يبتسم لك : [ ${value} ]
💰 الجائزة : +${prizeOrPenalty} ذهب
✨ رصيدك الحالي : ${newGold} ذهب
            `;
        } else {
            // خسارة
            prizeOrPenalty = -30;
            if (inventory.includes("درع الحصن 🛡️")) prizeOrPenalty = Math.floor(prizeOrPenalty * 0.5);
            if (inventory.includes("عباءة الظلال 🧥")) prizeOrPenalty = Math.floor(prizeOrPenalty * 0.8);

            const newGold = await db.update_user_gold(uid, prizeOrPenalty);
            resultText = `
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ خسارة ساحقة ⌯
┗━━━━━━━ ● ━━━━━━━┛

💀 الحظ : [ ${value} ]
💸 خسارتك : ${Math.abs(prizeOrPenalty)} ذهب
✨ رصيدك الحالي : ${newGold} ذهب
            `;
        }

        // إرسال النتيجة النهائية
        await ctx.reply(resultText);

        // تحقق من المهمة اليومية
        const missionCompleted = await db.complete_mission(uid, MISSION_TYPE);
        if (missionCompleted) {
            await db.add_to_inventory(uid, REWARD_ITEM);
            await ctx.reply(`✅ تم إكمال المهمة اليومية!\n🎁 تم إضافة ${REWARD_ITEM} إلى مخزونك`);
        }

    } catch (err) {
        console.error(err);
        await ctx.reply("❌ فشل في رمي النرد، حاول مرة أخرى");
    }
}

module.exports = { handle };
