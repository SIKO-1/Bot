# ملف: cmd_beauty_iraqi.py
import telebot
import random
import hashlib

COMMANDS = ["جمالي"]

# رموز حسب النسبة
EMOJIS = [
    (0, 20, "💀❌"),
    (21, 40, "😅🙃"),
    (41, 60, "🙂✨"),
    (61, 80, "😍🌟"),
    (81, 99, "🤩👑"),
    (100, 100, "👑🌹🔥")
]

# أوصاف باللهجة العراقية حسب النسبة
DESCRIPTIONS = [
    (0, 20, [
        "ههه، الظل يمشي احسن منك 😅",
        "الجمال مو كلشي، روحك اهم 🌫️"
    ]),
    (21, 40, [
        "ايه، زين شوية، بس مو كلش 😉",
        "ابتسامتك خفيفة، تكفي تفرّح 😏"
    ]),
    (41, 60, [
        "زين، وجيهك حلو، وقلبك أحلى ❤️",
        "توازن بين الزين والوسط 🌌"
    ]),
    (61, 80, [
        "واو، تلمع مثل الشمس ☀️",
        "إشراقتك تخلي الكل يدورلك 👀"
    ]),
    (81, 99, [
        "أنت وجه ساحر، والله 😍",
        "الجمال يمشي وياك وين ما رحت ✨"
    ]),
    (100, 100, [
        "👑 ملك/ة جمال الكون! محد يضاهيك",
        "🔥 الجمال المطلق، كلشي قدامك صغير"
    ])
]

def deterministic_score(uid):
    """يعطي نفس الشخص نسبة شبه ثابتة من 1-100"""
    hash_val = int(hashlib.sha256(str(uid).encode()).hexdigest(), 16)
    return (hash_val % 100) + 1

def get_emoji(score):
    for low, high, emoji in EMOJIS:
        if low <= score <= high:
            return emoji
    return "❔"

def get_description(score, uid):
    for low, high, options in DESCRIPTIONS:
        if low <= score <= high:
            return random.Random(uid + score).choice(options)
    return "🤔 نسبة غريبة"

def handle(bot, message):
    if message.text not in COMMANDS:
        return

    uid = message.from_user.id
    user_name = message.from_user.first_name

    score = deterministic_score(uid)
    desc = get_description(score, uid)
    emoji = get_emoji(score)

    try:
        photos = bot.get_user_profile_photos(uid, limit=1)
        if photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
            bot.send_photo(
                message.chat.id,
                file_id,
                caption=f"✨ جمال {user_name}: {score}/100 {emoji}\n{desc}"
            )
        else:
            bot.reply_to(message, f"✨ جمال {user_name}: {score}/100 {emoji}\n{desc}\n⚠️ ماكو صورة بالبروفايل")
    except Exception as e:
        bot.reply_to(message, f"❌ صار خطأ وانا جايب الصورة: {e}")
