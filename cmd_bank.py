# cmd_bank.py
from db_manager import get_user, update_user_gold, update_user_points, deposit_to_bank, withdraw_from_bank
import time
import random

COMMANDS = ["بنك", "رصيد_بنك", "سحب", "ايداع", "قرض", "فتح_حساب"]

INTEREST_RATE = 0.05  # فائدة 5% يومية
LOAN_INTEREST = 0.1   # فائدة القرض 10%

async def handle(bot, ctx):
    text = ctx.message.text.strip()
    if not text or not any(text.startswith(cmd) for cmd in COMMANDS):
        return

    uid = ctx.from_user.id
    user = await get_user(uid, name=ctx.from_user.first_name, username=ctx.from_user.username)

    # ===== فتح حساب بنكي =====
    if text.startswith("فتح_حساب"):
        if "bank_account" in user:
            await ctx.reply(f"🏦 لديك بالفعل حساب بنكي باسم: {user['bank_account']}")
            return
        account_name = ctx.from_user.first_name
        await deposit_to_bank(uid, 0)  # إنشاء حساب فارغ
        await ctx.bot.db.users_col.update_one({"uid": uid}, {"$set": {"bank_account": account_name, "bank_last_interest": time.time()}})
        await ctx.reply(f"✅ تم إنشاء حساب بنكي باسم: {account_name}")
        return

    # ===== تحديث الفوائد اليومية =====
    last_interest = user.get("bank_last_interest", 0)
    now = time.time()
    if now - last_interest >= 86400:  # يوم كامل
        balance = user.get("bank", 0)
        points = user.get("points", 0)
        interest_gold = int(balance * INTEREST_RATE)
        interest_points = int(points * INTEREST_RATE)
        if interest_gold > 0:
            await update_user_gold(uid, interest_gold)
        if interest_points > 0:
            await update_user_points(uid, interest_points)
        await ctx.bot.db.users_col.update_one({"uid": uid}, {"$set": {"bank_last_interest": now}})
        if interest_gold > 0 or interest_points > 0:
            await ctx.reply(f"💹 تم إضافة الفوائد اليومية: {interest_gold} ذهب و {interest_points} نقاط")

    # ===== رصيد البنك =====
    if text in ["بنك", "رصيد_بنك"]:
        bank_gold = user.get("bank", 0)
        points = user.get("points", 0)
        await ctx.reply(f"🏦 رصيدك في البنك: {bank_gold} \n نقاطك في البنك: {points} نقاط")
        return

    # ===== إيداع =====
    if text.startswith("ايداع"):
        parts = text.split()
        if len(parts) != 3 or not parts[2].isdigit() or parts[1] not in ["ذهب", "نقاط"]:
            await ctx.reply("⚠️ الصيغة: ايداع ذهب 500 أو ايداع نقاط 500")
            return
        amount = int(parts[2])
        if parts[1] == "ذهب":
            if await deposit_to_bank(uid, amount):
                await ctx.reply(f"✅ تم إيداع {amount} ذهب في البنك")
            else:
                await ctx.reply("❌ رصيدك لا يكفي")
        else:
            if user.get("points", 0) >= amount:
                await update_user_points(uid, -amount)
                await ctx.bot.db.users_col.update_one({"uid": uid}, {"$inc": {"bank_points": amount}})
                await ctx.reply(f" تم إيداع {amount} نقاط في البنك")
            else:
                await ctx.reply("❌ نقاطك لا تكفي")
        return

    # ===== سحب =====
    if text.startswith("سحب"):
        parts = text.split()
        if len(parts) != 3 or not parts[2].isdigit() or parts[1] not in ["ذهب", "نقاط"]:
            await ctx.reply("⚠️ الصيغة: سحب ذهب 300 أو سحب نقاط 300")
            return
        amount = int(parts[2])
        if parts[1] == "ذهب":
            if await withdraw_from_bank(uid, amount):
                await ctx.reply(f" تم سحب {amount} ذهب من البنك")
            else:
                await ctx.reply("❌ رصيد البنك لا يكفي")
        else:
            bank_points = user.get("bank_points", 0)
            if bank_points >= amount:
                await ctx.bot.db.users_col.update_one({"uid": uid}, {"$inc": {"bank_points": -amount}})
                await update_user_points(uid, amount)
                await ctx.reply(f"✅ تم سحب {amount} نقاط من البنك")
            else:
                await ctx.reply("❌ نقاط البنك لا تكفي")
        return

    # ===== قرض =====
    if text.startswith("قرض"):
        parts = text.split()
        if len(parts) != 3 or not parts[2].isdigit() or parts[1] not in ["فلوس", "نقاط"]:
            await ctx.reply("⚠️ الصيغة: قرض فلوس 500 أو قرض نقاط 500")
            return
        amount = int(parts[2])
        if parts[1] == "فلوس":
            await update_user_gold(uid, amount)
            await ctx.bot.db.users_col.update_one({"uid": uid}, {"$inc": {"bank_loan_gold": int(amount * (1 + LOAN_INTEREST))}})
            await ctx.reply(f"💳 تم منحك قرض {amount} فلوس بفائدة {int(LOAN_INTEREST*100)}%")
        else:
            await update_user_points(uid, amount)
            await ctx.bot.db.users_col.update_one({"uid": uid}, {"$inc": {"bank_loan_points": int(amount * (1 + LOAN_INTEREST))}})
            await ctx.reply(f"💳 تم منحك قرض {amount} نقاط بفائدة {int(LOAN_INTEREST*100)}%")
