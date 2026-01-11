// cmd_youtube.js
const { Telegraf } = require('telegraf');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

async function handle(ctx) {
    const text = ctx.message?.text?.trim();
    if (!text || !text.toLowerCase().startsWith('يوت ')) return;

    const query = text.slice(4).trim();
    if (!query) return ctx.reply("❌ اكتب اسم الأغنية بعد 'يوت'");

    const chatId = ctx.chat.id;
    const sentMsg = await ctx.reply("👑 الإمبراطور يبحث ويجهّز الصوت...");

    // مجلد مؤقت للملفات
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'yt-'));
    const outputTemplate = path.join(tempDir, '%(id)s.%(ext)s');

    try {
        // تحميل الصوت + الصورة باستخدام yt-dlp
        const cmd = `yt-dlp "ytsearch1:${query}" -x --audio-format opus --audio-quality 0 --output "${outputTemplate}" --write-thumbnail --no-playlist`;
        execSync(cmd, { stdio: 'ignore' });

        // البحث عن الملفات داخل tempDir
        const files = fs.readdirSync(tempDir);
        const audioFile = files.find(f => f.endsWith('.opus'));
        const thumbFile = files.find(f => f.endsWith('.jpg') || f.endsWith('.webp'));

        if (!audioFile) {
            return ctx.telegram.editMessageText(chatId, sentMsg.message_id, null, "❌ حدث خطأ أثناء تجهيز الصوت.");
        }

        const audioPath = path.join(tempDir, audioFile);
        const thumbPath = thumbFile ? path.join(tempDir, thumbFile) : null;

        const title = path.parse(audioFile).name;

        // إرسال الصوت كـ Voice مع الصورة واسم الأغنية
        if (thumbPath) {
            await ctx.telegram.sendVoice(chatId, { source: audioPath }, { caption: `🎵 ${title}`, thumb: { source: thumbPath } });
        } else {
            await ctx.telegram.sendVoice(chatId, { source: audioPath }, { caption: `🎵 ${title}` });
        }

        await ctx.telegram.deleteMessage(chatId, sentMsg.message_id);

    } catch (err) {
        await ctx.telegram.editMessageText(chatId, sentMsg.message_id, null, `❌ حدث خطأ: ${err.message}`);
    } finally {
        // حذف الملفات المؤقتة
        fs.rmSync(tempDir, { recursive: true, force: true });
    }
}

module.exports = { handle };
