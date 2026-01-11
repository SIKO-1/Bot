// bot.js
require('dotenv').config();
const { Telegraf } = require('telegraf');
const fs = require('fs');
const path = require('path');
const db = require('./db_manager');

// ======================
// الإعدادات الأساسية
// ======================
const BOT_TOKEN = process.env.BOT_TOKEN;

// المطورين (أنت + جماعتك)
const DEV_IDS = [
    5860391324,
    7076215547,
    7855813063
];

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
        if (
            !file.endsWith('.js') ||
            file === 'bot.js' ||
            file === 'db_manager.js'
        ) return;

        const moduleName = file.replace('.js', '');

        try {
            delete require.cache[require.resolve(path.join(basePath, file))];
            const mod = require(path.join(basePath, file));

            if (mod.handle) {
                if (file.startsWith('cmd_')) cmdModules[moduleName] = mod;
                if (file.startsWith('game_')) gameModules[moduleName] = mod;
            }

            console.log(`✅ تم تحميل: ${moduleName}`);
        } catch (err) {
            moduleErrors[file] = err.message;
            console.error(`⚠️ خطأ تحميل ${file}:\n`, err);

            DEV_IDS.forEach(id => {
                bot.telegram.sendMessage(
                    id,
                    `⚠️ خطأ تحميل:\n${file}\n${err.message}`
                ).catch(() => {});
            });
        }
    });
}

loadModules();

// ======================
// أدوات مساعدة
// ======================
function isDeveloper(uid) {
    return DEV_IDS.includes(uid);
}

// ======================
// /start
// ======================
bot.start(ctx => {
    console.log(`📩 /start من ${ctx.from.id}`);
    ctx.reply('👑 البوت شغال.');
});

// ======================
// التعامل مع الرسائل النصية
// ======================
bot.on('text', async ctx => {
    const uid = ctx.from.id;
    const text = ctx.message.text.trim();

    console.log(`📩 رسالة من ${uid}: ${text}`);

    // ===== تحديث الموديولات =====
    if (text === 'تحديث' && isDeveloper(uid)) {
        loadModules();

        let reply = '🔄 تم تحديث الموديولات\n\n✅ CMD:\n';
        reply += Object.keys(cmdModules).join('\n') || '—';
        reply += '\n\n🎮 GAME:\n';
        reply += Object.keys(gameModules).join('\n') || '—';

        if (Object.keys(moduleErrors).length > 0) {
            reply += '\n\n⚠️ أخطاء:\n';
            for (const [f, e] of Object.entries(moduleErrors)) {
                reply += `• ${f}: ${e}\n`;
            }
        }

        return ctx.reply(reply);
    }

    // ===== إعادة تشغيل =====
    if (['ريست', 'إعادة تشغيل'].includes(text) && isDeveloper(uid)) {
        ctx.reply('♻️ يتم إعادة تشغيل البوت...');
        console.log('♻️ إعادة تشغيل...');
        process.exit(0);
    }

    // ===== تمرير للأوامر =====
    for (const module of Object.values(cmdModules)) {
        try {
            module.handle(bot, ctx, db, DEV_IDS);
        } catch (err) {
            console.error('⚠️ خطأ CMD:', err);
        }
    }

    for (const module of Object.values(gameModules)) {
        try {
            module.handle(bot, ctx, db, DEV_IDS);
        } catch (err) {
            console.error('⚠️ خطأ GAME:', err);
        }
    }
});

// ======================
// الرسائل الخاصة
// ======================
bot.on('message', async ctx => {
    if (ctx.chat.type !== 'private') return;

    for (const module of Object.values(cmdModules)) {
        if (module.handlePrivate) {
            try {
                module.handlePrivate(bot, ctx, db, DEV_IDS);
            } catch (err) {
                console.error('⚠️ خطأ Private:', err);
            }
        }
    }
});

// ======================
// أزرار Inline
// ======================
bot.on('callback_query', async ctx => {
    for (const module of Object.values(cmdModules)) {
        if (module.handleCallback) {
            try {
                module.handleCallback(bot, ctx, db, DEV_IDS);
            } catch (err) {
                console.error('⚠️ خطأ Callback:', err);
            }
        }
    }
});

// ======================
// تشغيل البوت
// ======================
bot.launch().then(() => {
    console.log('🚀 البوت شغال وبكامل الهيبة');
});

// إغلاق آمن
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
