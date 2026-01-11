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
async function getUser(uid, name = null, username = null) {
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
            name: name,
            username: username,
            total_messages: 0,
            married_to: null,
            birthday: null,
            birthday_auto: true
        };
        await users.insertOne(user);
    } else {
        // تحديث الاسم واليوزر تلقائياً
        const updates = {};
        if (name && user.name !== name) updates.name = name;
        if (username && user.username !== username) updates.username = username;
        if (Object.keys(updates).length > 0) {
            await users.updateOne({ uid }, { $set: updates });
        }
    }

    return await users.findOne({ uid });
}

// ======================
// جلب جميع المستخدمين (مهم للإشعارات)
// ======================
async function getAllUsers() {
    return await users.find({}).project({ uid: 1 }).toArray();
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

// ======================
// المهام اليومية
// ======================
const DAY = 86400 * 1000;

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

    await users.updateOne(
        { uid },
        { $set: { box_ready: true, daily_task: null } }
    );
    return true;
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
// التصدير
// ======================
module.exports = {
    initDB,
    DEVELOPERS,
    getUser,
    getAllUsers,
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
    canGetTask,
    getDailyTask,
    completeMission,
    takeGift,
    isUserBanned,
    banUser,
    unbanUser
};
