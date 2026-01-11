# Dockerfile for Node.js Telegram Bot with yt-dlp support
FROM node:20-slim

# ======================
# تثبيت الأدوات الأساسية
# ======================
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ======================
# تثبيت yt-dlp
# ======================
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
    -o /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp

# ======================
# إعداد مجلد العمل
# ======================
WORKDIR /app

# ======================
# نسخ ملفات البوت وتثبيت dependencies
# ======================
COPY package*.json ./
RUN npm install --production

COPY . .

# ======================
# الأمر الافتراضي لتشغيل البوت
# ======================
CMD ["node", "bot.js"]
