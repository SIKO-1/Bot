# ملف: bot_commands.py
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db_manager import _get_user, get_user_gold
import random

# ======= إعداد المطورين =======
DEV_IDS = [5860391324, 7855813063, 7076215547]

# ======= الرتب =======
def get_user_rank_in_bot(uid):
    user = _get_user(uid)
    rank_val = user.get("rank", 0)
    if rank_val == 0:
        return "عضو"
    elif rank_val == 1:
        return "مشرف"
    elif rank_val >= 2:
        return "مالك / مطور"
    return "عضو"

# ======= جمل عشوائية للايدي =======
ID_QUOTES = [
    "مو كل اسم ينكتب… بعضهم ينحفر.",
    "الحضور ما يحتاج تعريف.",
    "الهيبة أسلوب، مو ضجيج.",
    "مكانك ثابت حتى لو تغيّر المكان.",
    "الصمت أحيانًا أفخم من الكلام.",
    "مو رقم… هو توقيع.",
    "الاسم بسيط، التأثير ثقيل.",
    "الهيبة ما تنشرح، تنفهم.",
    "مو نسخة، أصل.",
    "بعض الناس ما يحتاجون لقب."
]

# ======= نص القائمة الرئيسية =======
def MAIN_MENU_TEXT(name):
    return f"""
✮‍︙اوامــر البــوت الرئيسيـة
—————————————
✮‍︙م1 ← اوامر الحمايه
✮‍︙م2 ← اوامر التفعيل
✮‍︙م3 ← اوامر المسح
✮‍︙م4 ← اوامر الرفع
✮‍︙م5 ← اوامر المالكيـن
✮‍︙م6 ← اوامر الاعضاء
✮‍︙م7 ← اوامر المطور
✮‍︙م8 ← اوامـــر التسليـه
✮‍︙م9 ← اوامـــر البنـــــك
━━━━━━━━━━━━━━━
مرحباً بك يا {name}
"""

# ======= القوائم التفصيلية بالكامل =======
MENUS = {
    "م1": """⌔︙اوامر الحمايه كالاتي ...
—————————————
⌔︙قفل ، فتح ← الامر 
⌔︙تستطيع قفل حمايه كما يلي ...
⌔︙← { بالتقييد ، بالطرد ، بالكتم }
—————————————
⌔︙الكل ~ الدخول
⌔︙الروابط ~ المعرف
⌔︙التاك ~ الشارحه
⌔︙التعديل ~ تعديل الميديا
⌔︙المتحركه ~ الملفات
⌔︙الصور ~ الفيديو 
—————————————
⌔︙الماركداون ~ البوتات
⌔︙التكرار ~ الكلايش
⌔︙السيلفي ~ الملصقات
⌔︙الانلاين ~ الدردشه
⌔︙الهمسه
—————————————
⌔︙التوجيه ~ الاغاني
⌔︙الصوت ~ الجهات
⌔︙الاشعارات ~ التثبيت 
⌔︙الوسائط ~ التفليش
⌔︙وسائط المميزين
⌔︙الفشار ~ ارسال القناة
⌔︙القنوات ~ الموقع
⌔︙الإنكليزيه ~ الفارسيه
⌔︙الكفر ~ الاباحي
⌔︙التشويش ~ الملصقات المميزه
—————————————
⌔︙🏠 العودة للرئيسية""",

    "م2": """⌔︙اوامر ادمنية المجموعه ...
—————————————
⌔︙رفع، تنزيل ← مميز
⌔︙المميزين ← مسح المميزين
⌔︙رفع المالك 
⌔︙تاك ، تاك للكل ، المجموعه
⌔︙منع ، الغاء منع
—————————————
⌔︙الاوامر التالية ← {بالرد ، بالمعرف}
⌔︙حظر ، طرد ← الغاء حظر 
⌔︙كتم ← الغاء كتم
⌔︙تقييد ← الغاء تقييد
⌔︙كشف ، رفع ← القيود
⌔︙انذار ← {بالرد ، بالمعرف} 
—————————————
⌔︙عرض القوائم كما يلي ...
⌔︙المنشئين الاساسيين ، المنشئين
⌔︙المدراء ، الادمنيه ، المميزين
⌔︙المشرفين ، المكتومين
⌔︙قائمه المنع
—————————————
⌔︙🏠 العودة للرئيسية""",

    "م3": """⌔︙اوامر المدراء في المجموعه
—————————————
⌔︙رفع ، تنزيل ← ادمن
⌔︙الادمنيه ← مسح الادمنيه
⌔︙رفع الادمنيه 
⌔︙تنزيل الكل ← {بالرد ، بالمعرف}
⌔︙كشف ، طرد ، قفل ← البوتات
⌔︙قفل البوتات ← بالطرد
⌔︙فحص ← البوت
⌔︙طرد ← المحذوفين 
⌔︙قفل فتح ← القنوات
⌔︙مسح التعديل
—————————————
⌔︙🏠 العودة للرئيسية""",

    "م4": """⌔︙اوامر المنشئ الاساسي
—————————————
⌔︙رفع ، تنزيل ←{ منشئ }
⌔︙المنشئين ، مسح المنشئين
⌔︙رفع ، تنزيل ←{ مشرف }
⌔︙ضع لقب + لقب←{ بالرد }
⌔︙صلاحيات المجموعه
⌔︙صلاحيات المشرفين
⌔︙مسح نقاطه ، رسائله←{بالرد ، بالمعرف}
—————————————
⌔︙🏠 العودة للرئيسية""",

    "م5": """⌔︙اوامر مالك المجموعه
—————————————
⌔︙رفع ، تنزيل ←{ مالك }
⌔︙المالكين ، مسح المالكين
⌔︙ارفعني مالك
⌔︙رفع المالك (المالك اذا كان عضو يمكنه رفع نفسه)
⌔︙تنزيل جميع الرتب
⌔︙مسح الرتب الوهميه
—————————————
⌔︙🏠 العودة للرئيسية""",

    "م6": """︙اوامر التسليه كالاتي: 
—————————————
⌔︙غنيلي ، ريمكس ، اغنيه ، شعر
⌔︙قصيده ، صوره ، متحركه ، ميوزك
⌔︙انمي ، ميمز ، ستوري
⌔︙مسلسل ، فلم
⌔︙حساب العمر( احسب + تاريخ الميلاد)
⌔︙معنى اسم + الاسم
⌔︙اقتباس ، اذكار
—————————————
⌔︙🏠 العودة للرئيسية""",

    "م7": """︙اوامر البنك كالاتي :
—————————————
⌔︙انشاء ، مسح حساب بنكي
⌔︙راتب ، بخشيش
⌔︙استثمار + { رقم }
⌔︙مضاربه + { رقم }
⌔︙تحويل + رقم { بالرد }
—————————————
⌔︙🏠 العودة للرئيسية""",

    "م8": """︙اوامر التنظيف كالاتي: 
—————————————
⌔︙مسح + عدد ، مسح ←{ بالرد }
⌔︙الميديا ، مسح الميديا 
⌔︙امسح ، امسح + { عدد }
⌔︙تفعيل ، تعطيل ←{ امسح }
—————————————
⌔︙🏠 العودة للرئيسية""",

    "م9": """︙اوامر المطور
—————————————
⌔︙اضف فلوس + مبلغ {بالرد ، بالمعرف}  
⌔︙تصفير فلوسه { بالرد ، بالمعرف }
⌔︙تصفير الحراميه
⌔︙تصفير المتزوجين
⌔︙تصفير الفلوس
⌔︙مسح لعبه البنك
—————————————
⌔︙🏠 العودة للرئيسية"""
}

# ======= أزرار القائمة الرئيسية =======
def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("م1", callback_data="م1"),
        InlineKeyboardButton("م2", callback_data="م2"),
        InlineKeyboardButton("م3", callback_data="م3"),
        InlineKeyboardButton("م4", callback_data="م4"),
        InlineKeyboardButton("م5", callback_data="م5"),
        InlineKeyboardButton("م6", callback_data="م6"),
        InlineKeyboardButton("م7", callback_data="م7"),
        InlineKeyboardButton("م8", callback_data="م8"),
        InlineKeyboardButton("م9", callback_data="م9")
    )
    return keyboard

# ======= زر العودة للرئيسية =======
def back_to_main_keyboard():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="main_menu")
    )

# ======= التعامل مع الرسائل =======
async def handle_message(message: types.Message):
    uid = message.from_user.id
    rank = get_user_rank_in_bot(uid)
    text = message.text.strip()

    # الاوامر الرئيسية
    if text in ["اوامر", "الأوامر"]:
        if rank == "عضو":
            return
        await message.reply(
            MAIN_MENU_TEXT(message.from_user.first_name),
            reply_markup=main_menu_keyboard()
        )
        return

    # الايدي
    if text in ["ا", "ايدي"]:
        user = message.from_user
        if message.reply_to_message and uid in DEV_IDS:
            user = message.reply_to_message.from_user

        uid_user = user.id
        quote = random.choice(ID_QUOTES)
        gold = get_user_gold(uid_user)
        username = f"@{user.username}" if user.username else str(uid_user)
        bio = getattr(user, "bio", "")
        rank_user = get_user_rank_in_bot(uid_user)
        accountType = "حساب مميز" if getattr(user, "is_premium", False) else "حساب عادي"

        text_id = f"""
↫ {quote}

⌁︙ايديڪ↫ {uid_user}
⌁︙معرفڪ↫ {username}
⌁︙حسابڪ↫ {accountType}
⌁︙رتبتڪ بالبـوت↫ {rank_user}
⌁︙فلوسڪ↫ {gold} ذهب
⌁︙البـايـــو↫ {bio}
"""
        await message.reply(text_id)
        return

# ======= التعامل مع أزرار القوائم =======
async def handle_callback(callback: types.CallbackQuery):
    uid = callback.from_user.id
    rank = get_user_rank_in_bot(uid)
    data = callback.data

    if rank == "عضو":
        return

    if data == "main_menu":
        await callback.message.edit_text(
            MAIN_MENU_TEXT(callback.from_user.first_name),
            reply_markup=main_menu_keyboard()
        )
        await callback.answer()
        return

    if data in MENUS:
        await callback.message.edit_text(
            MENUS[data],
            reply_markup=back_to_main_keyboard()
        )
        await callback.answer()
