// db_manager.js
const { MongoClient } = require('mongodb');

const MONGO_URI = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?retryWrites=true&w=majority";
const DB_NAME = "imperial_bot";

let db, users;

async function initDB() {
    const client = new MongoClient(MONGO_URI);
    try {
        await client.connect();
        db = client.db(DB_NAME);
        users = db.collection("users");
        console.log("✅ MongoDB متصل بنجاح!");
    } catch (err) {
        console.error("❌ فشل الاتصال بـ MongoDB:", err);
    }
}

// ======================
// المطورين
// ======================
const DEVELOPERS = [7076215547, 7855813063, 5860391324];

// ======================
// المستخدمين
// ======================
async function getUser(uid) {
    let user = await users.findOne({ uid });
    if (!user) {
        user = {
            uid,
            gold: 0,
            bank: 0,
            inventory: [],
            rank: 0,
            last_task_time: 0,
            daily_task: null,
            box_ready: false,
            box_opened: false,
            last_gift_time: 0,
            banned: false,
            name: null,
            username: null,
            total_messages: 0,
            married_to: null
        };
        await users.insertOne(user);
    }
    return await users.findOne({ uid });
}

// ======================
// الذهب
// ======================
async function getUserGold(uid) {
    const user = await getUser(uid);
    return user.gold;
}

async function updateUserGold(uid, amount) {
    const user = await getUser(uid);
    const newGold = Math.max(0, user.gold + amount);
    await users.updateOne({ uid }, { $set: { gold: newGold } });
    return newGold;
}

// ======================
// البنك
// ======================
async function getUserBank(uid) {
    const user = await getUser(uid);
    return user.bank;
}

async function depositToBank(uid, amount) {
    const user = await getUser(uid);
    if (amount <= 0 || user.gold < amount) return false;
    await users.updateOne({ uid }, { $inc: { gold: -amount, bank: amount } });
    return true;
}

async function withdrawFromBank(uid, amount) {
    const user = await getUser(uid);
    if (amount <= 0 || user.bank < amount) return false;
    await users.updateOne({ uid }, { $inc: { bank: -amount, gold: amount } });
    return true;
}

// ======================
// المخزون
// ======================
async function getInventory(uid) {
    const user = await getUser(uid);
    return user.inventory || [];
}

async function addToInventory(uid, item, quantity = 1) {
    const user = await getUser(uid);
    const newInv = [...user.inventory, ...Array(quantity).fill(item)];
    await users.updateOne({ uid }, { $set: { inventory: newInv } });
}

async function removeFromInventory(uid, item, quantity = 1) {
    const user = await getUser(uid);
    let count = 0;
    const newInv = [];
    for (let i of user.inventory) {
        if (i === item && count < quantity) {
            count++;
            continue;
        }
        newInv.push(i);
    }
    await users.updateOne({ uid }, { $set: { inventory: newInv } });
    return count === quantity;
}

// ======================
// الرتب
// ======================
async function getUserRank(uid) {
    const user = await getUser(uid);
    return user.rank || 0;
}

async function setUserRank(uid, rank) {
    await users.updateOne({ uid }, { $set: { rank } });
}

async function downgradeUserRank(byUid, targetUid, newRank) {
    if (!DEVELOPERS.includes(byUid)) return { ok: false, error: "❌ هذا الأمر للمطور فقط." };
    if (newRank < 0) newRank = 0;

    const target = await getUser(targetUid);
    const oldRank = target.rank || 0;
    if (newRank >= oldRank) return { ok: false, error: "⚠️ لا يمكن التخفيض لنفس الرتبة أو أعلى." };

    await users.updateOne({ uid: targetUid }, { $set: { rank: newRank } });
    return { ok: true, old_rank: oldRank, new_rank: newRank };
}

// ======================
// المهام اليومية
// ======================
const DAY = 86400 * 1000; // 24 ساعة بالميلي ثانية
const TASKS = [
    { type: "dice", desc: "العب لعبة النرد 🎲" },
    { type: "roulette", desc: "العب روليت 🎰" }
];

async function canGetTask(uid) {
    const user = await getUser(uid);
    return Date.now() - user.last_task_time >= DAY;
}

async function getDailyTask(uid) {
    const user = await getUser(uid);
    if (user.daily_task) return user.daily_task;
    if (!(await canGetTask(uid))) return null;

    const task = TASKS[Math.floor(Math.random() * TASKS.length)];
    await users.updateOne(
        { uid },
        { $set: { daily_task: task, last_task_time: Date.now(), box_ready: false, box_opened: false } }
    );
    return task;
}

async function completeMission(uid, missionType) {
    const user = await getUser(uid);
    if (!user.daily_task || user.daily_task.type !== missionType) return false;
    await users.updateOne({ uid }, { $set: { box_ready: true, daily_task: null } });
    return true;
}

async function canOpenBox(uid) {
    const user = await getUser(uid);
    return user.box_ready && !user.box_opened;
}

async function setBoxOpened(uid) {
    await users.updateOne({ uid }, { $set: { box_opened: true } });
}

// ======================
// الهدايا اليومية
// ======================
async function takeGift(uid, amount = 100) {
    const user = await getUser(uid);
    if (Date.now() - user.last_gift_time < DAY) return null;
    await updateUserGold(uid, amount);
    await users.updateOne({ uid }, { $set: { last_gift_time: Date.now() } });
    return await getUserGold(uid);
}

// ======================
// الحظر
// ======================
async function isUserBanned(uid) {
    const user = await getUser(uid);
    return user.banned || false;
}

async function banUser(uid) {
    await users.updateOne({ uid }, { $set: { banned: true } });
}

async function unbanUser(uid) {
    await users.updateOne({ uid }, { $set: { banned: false } });
}

// ======================
// إحصائيات
// ======================
async function getAllUsersCount() {
    return await users.countDocuments();
}

// ======================
// أعياد الميلاد
// ======================
async function addBirthday(uid, day, month, year = null) {
    if (day < 1 || day > 31 || month < 1 || month > 12) return { ok: false, error: "⚠️ التاريخ غير صالح." };
    await users.updateOne({ uid }, { $set: { birthday: { day, month, year } } });
    return { ok: true, uid, birthday: { day, month, year } };
}

async function removeBirthday(uid) {
    await users.updateOne({ uid }, { $unset: { birthday: "" } });
    return { ok: true, uid };
}

async function getBirthday(uid) {
    const user = await getUser(uid);
    return user.birthday || null;
}

async function listBirthdays() {
    return await users.find({ birthday: { $exists: true } }).toArray();
}

async function enableBirthdayAuto(uid) {
    await users.updateOne({ uid }, { $set: { birthday_auto: true } });
    return { ok: true, uid };
}

async function disableBirthdayAuto(uid) {
    await users.updateOne({ uid }, { $set: { birthday_auto: false } });
    return { ok: true, uid };
}

async function isBirthdayAutoEnabled(uid) {
    const user = await getUser(uid);
    return user.birthday_auto || false;
}

module.exports = {
    initDB,
    DEVELOPERS,
    getUser,
    getUserGold,
    updateUserGold,
    getUserBank,
    depositToBank,
    withdrawFromBank,
    getInventory,
    addToInventory,
    removeFromInventory,
    getUserRank,
    setUserRank,
    downgradeUserRank,
    canGetTask,
    getDailyTask,
    completeMission,
    canOpenBox,
    setBoxOpened,
    takeGift,
    isUserBanned,
    banUser,
    unbanUser,
    getAllUsersCount,
    addBirthday,
    removeBirthday,
    getBirthday,
    listBirthdays,
    enableBirthdayAuto,
    disableBirthdayAuto,
    isBirthdayAutoEnabled
};
