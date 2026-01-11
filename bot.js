// bot.js
require('dotenv').config();
const { Telegraf } = require('telegraf');
const fs = require('fs');
const path = require('path');
const db = require('./db_manager');

const BOT_TOKEN = process.env.BOT_TOKEN;
const DEV_IDS = process.env.DEV_IDS ? process.env.DEV_IDS.split(',').map(id => parseInt(id.trim())) : [];

if (!BOT_TOKEN) throw new Error('❌ BOT_TOKEN غير موجود');

const bot = new Telegraf(BOT_TOKEN);

// ======================
// تهيئة قاعدة البيانات
// ======================
db.initDB();

// ======================
// الموديولات
// ======================
let cmdModules = {};
let gameModules = {};
let moduleErrors = {};

function loadModules() {
    cmdModules = {};
    gameModules = {};
    moduleErrors = {};

    const basePath = __dirname;
    console.log('📦 جاري تحميل الموديولات...');

    fs.readdirSync(basePath).forEach(file => {
        if (!file.endsWith('.js') || file === 'bot.js' || file === 'db_manager.js') return;

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
    const text = ctx.message.text.trim();

    console.log(`📩 رسالة من ${uid}: ${text}`);

    // تحديث الموديولات
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

    // إعادة تشغيل البوت
    if (['ريست', 'إعادة تشغيل'].includes(text) && DEV_IDS.includes(uid)) {
        ctx.reply('♻️ يتم إعادة تشغيل البوت...');
        console.log('♻️ إعادة تشغيل البوت...');
        process.exit(0);
    }

    // تمرير الرسائل لبقية الموديولات
    for (const [moduleName, module] of Object.entries(cmdModules)) {
        try {
            module.handle(bot, ctx, db);
        } catch (err) {
            console.error(`⚠️ خطأ في CMD ${moduleName}:\n`, err);
            DEV_IDS.forEach(id => {
                bot.telegram.sendMessage(id, `⚠️ خطأ في CMD ${moduleName}:\n${err.message}`).catch(() => {});
            });
        }
    }

    for (const [moduleName, module] of Object.entries(gameModules)) {
        try {
            module.handle(bot, ctx, db);
        } catch (err) {
            console.error(`⚠️ خطأ في GAME ${moduleName}:\n`, err);
            DEV_IDS.forEach(id => {
                bot.telegram.sendMessage(id, `⚠️ خطأ في GAME ${moduleName}:\n${err.message}`).catch(() => {});
            });
        }
    }
});

// ======================
// الرسائل الخاصة للموديولات
// ======================
bot.on('message', async ctx => {
    if (ctx.chat.type === 'private') {
        for (const [moduleName, module] of Object.entries(cmdModules)) {
            if (module.handlePrivate) {
                try {
                    module.handlePrivate(bot, ctx, db);
                } catch (err) {
                    console.error(`⚠️ خطأ في handlePrivate ${moduleName}:\n`, err);
                }
            }
        }
    }
});

// ======================
// أزرار Inline للموديولات
// ======================
bot.on('callback_query', async ctx => {
    for (const [moduleName, module] of Object.entries(cmdModules)) {
        if (module.handleCallback) {
            try {
                module.handleCallback(bot, ctx, db);
            } catch (err) {
                console.error(`⚠️ خطأ في handleCallback ${moduleName}:\n`, err);
            }
        }
    }
});

// ======================
// تشغيل البوت
// ======================
bot.launch().then(() => console.log('🚀 البوت شغال، جاري الاستماع للرسائل...'));

// التعامل مع الإغلاق بشكل آمن
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
