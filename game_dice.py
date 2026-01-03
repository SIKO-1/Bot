import time
import db_manager # الربط الصحيح مع الذاكرة الداخلية

def register_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text == "نرد")
    def dice_game(m):
        uid = m.from_user.id
        # جلب الذهب الحقيقي من النظام الداخلي
        user_gold = db_manager.get_user_gold(uid)

        # رسالة التمهيد
        start_msg = bot.reply_to(m, "🎲 جاري رمي نرد الحظ الإمبراطوري... استعد!")
        
        # إرسال النرد
        dice_msg = bot.send_dice(m.chat.id)
        value = dice_msg.dice.value 

        # انتظار توقف النرد
        time.sleep(3.5)

        if value >= 5:
            # الفوز (5 أو 6) - إضافة 200 ذهبة
            prize = 200
            db_manager.update_user_gold(uid, prize)
            res_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ فـوز إمـبـراطـوري ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"🔥 الـحـظ يـبـتـسـم لـك : [ {value} ]\n"
                f"💰 الـجـائزة : +{prize} ذهـبـة\n"
                f"✨ رصـيـدك الـحـالي : {user_gold + prize}"
            )
            bot.reply_to(dice_msg, res_text)
            
        elif value >= 3:
            # الربح المتوسط (3 أو 4) - إضافة 50 ذهبة
            prize = 50
            db_manager.update_user_gold(uid, prize)
            res_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ حـظ مـتـوسـط ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"🎲 الـنـتـيـجـة مـقـبـولـة : [ {value} ]\n"
                f"💰 الـجـوائـز : +{prize} ذهـبـة\n"
                f"✨ رصـيـدك الـحـالي : {user_gold + prize}"
            )
            bot.reply_to(dice_msg, res_text)
            
        else:
            # الخسارة (1 أو 2) - خصم 30 ذهبة
            penalty = -30
            db_manager.update_user_gold(uid, penalty)
            res_text = (
                "┏━━━━━━━ ● ━━━━━━━┓\n"
                "         ⌯ غـضـب الـنـرد ⌯\n"
                "┗━━━━━━━ ● ━━━━━━━┛\n\n"
                f"🌚 لـلأسـف حـظـك عـاثـر : [ {value} ]\n"
                f"💸 ضـريـبـة الـحـظ : {penalty} ذهـبـة\n"
                f"✨ رصـيـدك الـمـتـبـقي : {max(0, user_gold + penalty)}"
            )
            bot.reply_to(dice_msg, res_text)
        
        # تنظيف الشات
        try: bot.delete_message(m.chat.id, start_msg.message_id)
        except: pass
