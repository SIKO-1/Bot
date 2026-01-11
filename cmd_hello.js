// ملف: cmd_hello.js
const COMMANDS = ["هلا", "امداك", "مح", "محح", "مححححح", "انجب", "نعم", "ولاشي", "ولاشيء"];

async function handle(bot, msg) {
    if (!msg.text) return;

    const text = msg.text.trim().toLowerCase();
    const user = msg.from.first_name || "صديقي";

    // ======= الردود على الرسائل =======
    switch (text) {
        case "هلا":
            bot.sendMessage(msg.chat.id, `هلوات 🫦 يا ${user}`);
            break;

        case "امداك":
            bot.sendMessage(msg.chat.id, `امداك انتَ وقت 😎`);
            break;

        case "مح":
        case "محح":
        case "مححححح":
            bot.sendMessage(msg.chat.id, "عسسللل 🍯");
            break;

        case "انجب":
            bot.sendMessage(msg.chat.id, "انجب انتَ لا تنسحل 😏");
            break;

        case "نعم":
            bot.sendMessage(msg.chat.id, "لا 🙃");
            break;

        case "ولاشي":
        case "ولاشيء":
            bot.sendMessage(msg.chat.id, "لا، في شيء مو بكيفك 😌");
            break;

        default:
            // ===== ردود عشوائية عراقية =====
            const funReplies = [
                `شلونك يا ${user}؟ 😎`,
                `هاه شكو ماكو؟ 🤔`,
                `عيونك حلوة اليوم 👀`,
                `والله الجو حلو هسه 🌤`,
                `هاي، تحية إمبراطورية لك 👑`,
                `ههههه شكو هاي؟ 😂`
            ];
            const reply = funReplies[Math.floor(Math.random() * funReplies.length)];
            bot.sendMessage(msg.chat.id, reply);
            break;
    }
}

// ======= الترحيب بالعضو الجديد =======
async function handleNewMember(bot, msg) {
    if (!msg.new_chat_members || msg.new_chat_members.length === 0) return;

    for (const newMember of msg.new_chat_members) {
        const name = newMember.first_name || "عضو جديد";
        const welcomeMsg = `✨ نورتنا يا [${name}](tg://user?id=${newMember.id})! 👑`;
        bot.sendMessage(msg.chat.id, welcomeMsg, { parse_mode: "Markdown" });
    }
}

module.exports = { handle, handleNewMember };
