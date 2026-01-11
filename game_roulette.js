// game_roulette.js
const db = require('./db_manager');

const COMMAND = "روليت";
const MISSION_TYPE = "roulette";
const REWARD_ITEM = "🎁 صندوق الحظ النادر";

async function handle(bot, ctx) {
    if (!ctx.message.text.startsWith(COMMAND)) return;

    const uid = ctx.from.id;
    const userGold = await db.get_user_gold(uid);

    // ───────── 1. التحقق من الرهان ─────────
    const parts = ctx.message.text.split(" ");
    if (parts.length < 2) {
        return ctx.reply(
            "⚠️ يجب تحديد مبلغ الرهان\n💡 مثال: روليت 500"
        );
    }

    const bet = parseInt(parts[1]);
    if (isNaN(bet)) return ctx.reply("❌ الرهان يجب أن يكون رقماً صحيحاً");
    if (bet <= 0) return ctx.reply("🚫 لا يمكنك الرهان بمبلغ صفر أو أقل");
    if (bet > userGold) return ctx.reply(`💸 رصيدك الحالي: ${userGold} ذهب\n❌ لا تملك ذهباً كافياً`);

    // ───────── 2. واجهة اللعب ─────────
    let startText = `
┏━━━━━━━ ● ━━━━━━━┓
      🎰 روليت الإمبراطورية 🎰
┗━━━━━━━ ● ━━━━━━━┛

💰 الرهان: ${bet} ذهبة
🌀 تدوير عجلة القدر...
    `;
    let statusMsg = await ctx.reply(startText);

    await new Promise(r => setTimeout(r, 1500));
    await bot.editMessageText(ctx.chat.id, statusMsg.message_id, startText + "\n\n⚡️ العجلة تتباطأ...");
    await new Promise(r => setTimeout(r, 1500));

    // ───────── 3. تحديد النتيجة ─────────
    const outcome = ["win", "lose", "jackpot"];
    const weights = [45, 50, 5];

    function weightedRandom(items, weights) {
        const sum = weights.reduce((a, b) => a + b, 0);
        let r = Math.random() * sum;
        for (let i = 0; i < items.length; i++) {
            if (r < weights[i]) return items[i];
            r -= weights[i];
        }
    }

    const result = weightedRandom(outcome, weights);

    // ───────── 4. النتائج ─────────
    let resultText = "";
    let newBal = userGold;

    if (result === "win") {
        newBal = await db.update_user_gold(uid, bet);
        resultText = `
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ فـوز إمـبـراطـوري ⌯
┗━━━━━━━ ● ━━━━━━━┛

🔥 الحظ يبتسم لك : [ الفوز ]
💰 الجائزة : +${bet} ذهب
✨ رصيدك الحالي : ${newBal} ذهب
        `;
    } else if (result === "jackpot") {
        const jackpot = bet * 5;
        newBal = await db.update_user_gold(uid, jackpot);
        resultText = `
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ جاكبوت أسطوري ⌯
┗━━━━━━━ ● ━━━━━━━┛

🔥 الحظ يبتسم لك : [ الجاكبوت ]
💰 الجائزة : +${jackpot} ذهب
✨ رصيدك الحالي : ${newBal} ذهب
        `;
    } else {
        newBal = await db.update_user_gold(uid, -bet);
        resultText = `
┏━━━━━━━ ● ━━━━━━━┓
         ⌯ خسارة ساحقة ⌯
┗━━━━━━━ ● ━━━━━━━┛

💀 الحظ : [ الخسارة ]
💸 خسارتك : -${bet} ذهب
✨ رصيدك الحالي : ${newBal} ذهب
        `;
    }

    await bot.editMessageText(ctx.chat.id, statusMsg.message_id, resultText);

    // ───────── 5. التحقق من المهمة اليومية ─────────
    const missionCompleted = await db.complete_mission(uid, MISSION_TYPE);
    if (missionCompleted) {
        await db.add_to_inventory(uid, REWARD_ITEM);
        await ctx.reply(`✅ تم إكمال المهمة اليومية!\n🎁 تم إضافة ${REWARD_ITEM} إلى مخزونك`);
    }
}

module.exports = { handle };
