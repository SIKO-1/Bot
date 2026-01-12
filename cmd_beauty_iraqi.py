# cmd_beauty_iraqi.py
import hashlib

COMMANDS = ["جمالي"]

def deterministic_score(uid: int) -> int:
    """يعطي نسبة ثابتة لكل شخص حسب الـUID"""
    hash_bytes = hashlib.sha256(str(uid).encode()).hexdigest()
    num = int(hash_bytes[:8], 16)
    return (num % 100) + 1

async def handle(bot, ctx):
    if not ctx.message or not ctx.message.text:
        return

    text = ctx.message.text.strip()
    if text not in COMMANDS:
        return

    user_id = ctx.from_user.id
    score = deterministic_score(user_id)

    caption = f"⌔︙ الاسم: \n⌔︙ نسبة جمالك هي: {score}%"

    try:
        photos = await bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            # نأخذ أفضل جودة للصورة
            file_id = photos.photos[0][-1].file_id
            await ctx.reply_photo(file_id, caption=caption)
        else:
            await ctx.reply(caption)
    except:
        await ctx.reply(caption)
