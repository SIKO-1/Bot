import random
import time
from telebot import types

# نظام النقاط المرتبط بالـ Volume
try:
    from db_manager import get_user, update_user
except:
    def get_user(uid): return {"balance": 1000}
    def update_user(uid, k, v): pass

def register_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text == "نرد")
    def dice_game(m):
        uid = m.from_user.id
        user_bal = get_user(uid).get("balance", 0)

        # رسالة تمهيدية لرفع الحماس
        start_msg = bot.reply_to(m, "🎲 جاري رمي نرد الحظ الإمبراطوري... استعد!")
        
        # إرسال النرد المتحرك
        dice_msg = bot.send_dice(m.chat.id)
        value = dice_msg.dice.value # القيمة من 1 إلى 6

        # ننتظر 3 ثوانٍ حتى يتوقف النرد عن الدوران (لمسة واقعية ملكية)
        time.sleep(3.5)

        if value >= 5:
            # الفوز العظيم (5 أو 6)
            prize = 200
            update_user(uid, "balance", user_bal + prize)
            res_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ فـوز إمـبـراطـوري ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"🔥 الـحـظ يـبـتـسـم لـك : [ {value} ]\n"
                "💰 الـجـائزة الـكـبـرى : +200 نـقـطـة\n"
                f"✨ رصـيـدك الـحـالي : {user_bal + prize}"
            )
            bot.reply_to(dice_msg, res_text)
            
        elif value >= 3:
            # الربح المتوسط (3 أو 4)
            prize = 50
            update_user(uid, "balance", user_bal + prize)
            res_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ حـظ مـتـوسـط ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"🎲 الـنـتـيـجـة مـقـبـولـة : [ {value} ]\n"
                "💰 الـجـوائـز : +50 نـقـطـة\n"
                f"✨ رصـيـدك الـحـالي : {user_bal + prize}"
            )
            bot.reply_to(dice_msg, res_text)
            
        else:
            # غضب الحظ (1 أو 2)
            penalty = 30
            new_bal = max(0, user_bal - penalty)
            update_user(uid, "balance", new_bal)
            res_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ غـضـب الـنـرد ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"🌚 لـلأسـف حـظـك عـاثـر : [ {value} ]\n"
                "💸 ضـريـبـة الـحـظ : -30 نـقـطـة\n"
                f"✨ رصـيـدك الـمـتـبـقي : {new_bal}"
            )
            bot.reply_to(dice_msg, res_text)
        
        # حذف رسالة التمهيد لتنظيف الشات
        try: bot.delete_message(m.chat.id, start_msg.message_id)
        except: pass
