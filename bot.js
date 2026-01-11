// bot.js
require('dotenv').config();
const { Telegraf } = require('telegraf');
const fs = require('fs');
const path = require('path');

const BOT_TOKEN = process.env.BOT_TOKEN;
const DEV_IDS = process.env.DEV_IDS ? process.env.DEV_IDS.split(',').map(id => id.trim()) : [];

if (!BOT_TOKEN) throw new Error('❌ BOT_TOKEN غير موجود');

const bot = new Telegraf(BOT_TOKEN);

// ======================
// الموديولات
// ======================
const cmdModules = {};
const gameModules = {};
const moduleErrors = {};

function loadModules() {
    cmdModules = {};
    gameModules = {};
    moduleErrors = {};

    const basePath = __dirname;
    console.log('📦 جاري تحميل الموديولات...');

    fs.readdirSync(basePath).forEach(file => {
        if (!file.endsWith('.js') || file === 'bot.js') return;

        const moduleName = file.replace('.js', '');
        try {
            const mod = require(path.join(basePath, file));
            if (mod.handle) {
                if (file.startsWith('cmd_')) cmdModules[moduleName] = mod;
                if (file.startsWith('game_')) gameModules[moduleName] = mod;
            }
            console.log(`✅ تم تحميل الموديول: ${moduleName}`);
        } catch (err) {
            moduleErrors[file] = err.message;
            console.error(`⚠️ خطأ تحميل الموديول ${file}:\n`, err);
            DEV_IDS.forEach(id => {
                bot.telegram.sendMessage(id, `⚠️ خطأ تحميل:\n${file}\n${err.message}`).catch(() => {});
            });
        }
    });
}

loadModules();

// ======================
// أدوات مساعدة
// ======================
async function isAdmin(ctx, userId) {
    try {
        const member = await ctx.getChatMember(userId);
        return ['administrator', 'creator'].includes(member.status);
    } catch {
        return false;
    }
}

// ======================
// /start
// ======================
bot.start(ctx => {
    console.log(`📩 أمر /start من: ${ctx.from.id}`);
    ctx.reply('👑 البوت شغال.');
});

// ======================
// التعامل مع الرسائل
// ======================
bot.on('text', async ctx => {
    const uid = ctx.from.id;
    const chatId = ctx.chat.id;
    const text = ctx.message.text.trim();

    console.log(`📩 رسالة من ${uid} في ${chatId}: ${text}`);

    // أمر تحديث الموديولات
    if (text.toLowerCase() === 'تحديث' && DEV_IDS.includes(uid)) {
        loadModules();
        let reply = '🔄 تم تحديث الموديولات\n\n✅ CMD:\n';
        reply += Object.keys(cmdModules).join('\n') + '\n\n🎮 GAME:\n';
        reply += Object.keys(gameModules).join('\n');

        if (Object.keys(moduleErrors).length > 0) {
            reply += '\n\n⚠️ أخطاء:\n';
            for (const [fname, err] of Object.entries(moduleErrors)) {
                reply += `• ${fname}: ${err}\n`;
            }
        }

        ctx.reply(reply);
        return;
    }

    // أمر ريست البوت
    if (['ريست', 'إعادة تشغيل'].includes(text) && DEV_IDS.includes(uid)) {
        ctx.reply('♻️ يتم إعادة تشغيل البوت...');
        console.log('♻️ إعادة تشغيل البوت...');
        process.exit(0);
    }

    // تمرير الرسائل لبقية الموديولات
    for (const [moduleName, module] of Object.entries(cmdModules)) {
        try {
            module.handle(bot, ctx);
        } catch (err) {
            console.error(`⚠️ خطأ في موديول CMD ${moduleName}:\n`, err);
            DEV_IDS.forEach(id => {
                bot.telegram.sendMessage(id, `⚠️ خطأ في تنفيذ CMD ${moduleName}:\n${err.message}`).catch(() => {});
            });
        }
    }

    for (const [moduleName, module] of Object.entries(gameModules)) {
        try {
            module.handle(bot, ctx);
        } catch (err) {
            console.error(`⚠️ خطأ في موديول GAME ${moduleName}:\n`, err);
            DEV_IDS.forEach(id => {
                bot.telegram.sendMessage(id, `⚠️ خطأ في تنفيذ GAME ${moduleName}:\n${err.message}`).catch(() => {});
            });
        }
    }
});

// ======================
// تشغيل البوت
// ======================
bot.launch().then(() => console.log('🚀 البوت شغال، جاري الاستماع للرسائل...'));
