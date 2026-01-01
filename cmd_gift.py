from datetime import datetime, timedelta
from db_manager import get_user, update_user

def register_handlers(bot):
    """دالة التسجيل التلقائي"""
    
    # --- أمر الهدية المعدل ---
    @bot.message_handler(func=lambda message: message.text == "هدية")
    def gift_command(message):
        uid = message.from_user.id
        user = get_user(uid)
        now = datetime.now()
        
        last_gift_str = user.get("last_gift")
        if last_gift_str:
            last_time = datetime.fromisoformat(last_gift_str)
            if now < last_time + timedelta(days=1):
                # حساب الوقت المتبقي
                diff = (last_time + timedelta(days=1)) - now
                hours = int(diff.total_seconds() // 3600)
                minutes = int((diff.total_seconds() % 3600) // 60)
                
                msg = f"🌚 باقيلك {hours} ساعة و {minutes} دقيقة وتحصل هديتك ثانية.. لا تصير طماع! امشي العب وحصل نقاط ادبسز 🏃‍♂️"
                return bot.reply_to(message, msg)

        # إضافة النقاط
        new_balance = user.get("balance", 0) + 500
        update_user(uid, "balance", new_balance)
        update_user(uid, "last_gift", now.isoformat())
        
        bot.reply_to(message, f"🎁 هاك هذي 500 نقطة هدية.. \n💰 صار عندك {new_balance} نقطة، لا تصرفها كلها مرة وحدة!")

    # --- أمر الرصيد المعدل (فلوسي / رصيدي / رصيد) ---
    @bot.message_handler(func=lambda message: message.text in ["فلوسي", "رصيدي", "رصيد"])
    def balance_command(message):
        user = get_user(message.from_user.id)
        balance = user.get("balance", 0)
        
        if balance > 1000:
            msg = f"💰 رصيدك: {balance} نقطة\n🔥 أوهووو! عندك كثير فلوس يا غني، من أين لك هذا؟ 🤑"
        else:
            msg = f"💰 رصيدك: {balance} نقطة\n💸 هذي كل فلوسك؟ يا فقير شد حيلك وجمع نقاط! 🤡"
            
        bot.reply_to(message, msg)
