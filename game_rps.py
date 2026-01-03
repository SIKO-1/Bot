import random
from telebot import types
import db_manager # الربط بالخزنة الملكية

def register_handlers(bot):
    
    pvp_games = {}
    choices_map = {'r': '🪨 حجرة', 'p': '📜 ورقة', 's': '✂️ مقص'}

    @bot.message_handler(func=lambda m: m.text.split()[0] in ['حجره', 'حجرة', 'مقص', 'ورقة', 'ورقه', 'حجر'])
    def start_rps(m):
        uid = m.from_user.id
        args = m.text.split()
        
        # --- نظام اللعب ضد صديق (تحدي) ---
        if m.reply_to_message:
            opponent = m.reply_to_message.from_user
            if opponent.id == bot.get_me().id:
                return bot.reply_to(m, "⚠️ إذا أردت اللعب معي، اكتب 'حجرة' بدون رد (Reply)!")
            if opponent.id == uid:
                return bot.reply_to(m, "❌ لا يمكنك تحدي نفسك!")

            game_id = f"{uid}_{opponent.id}_{m.message_id}"
            pvp_games[game_id] = {
                "p1": uid, "p2": opponent.id,
                "p1_choice": None, "p2_choice": None,
                "p1_name": m.from_user.first_name, "p2_name": opponent.first_name
            }
            
            markup = types.InlineKeyboardMarkup()
            markup.row(
                types.InlineKeyboardButton("🪨 حجرة", callback_data=f"pvp_{game_id}_r"),
                types.InlineKeyboardButton("📜 ورقة", callback_data=f"pvp_{game_id}_p"),
                types.InlineKeyboardButton("✂️ مقص", callback_data=f"pvp_{game_id}_s")
            )
            bot.send_message(m.chat.id, f"⚔️ **تحدي الإمبراطورية بدأ!**\n\n👤 [{m.from_user.first_name}](tg://user?id={uid})\n🆚 [{opponent.first_name}](tg://user?id={opponent.id})\n\n💰 الجائزة: 50 ذهبة\n📥 اختارا سلاحكما الآن..", reply_markup=markup, parse_mode="Markdown")
            return

        # --- نظام اللعب ضد البوت ---
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("🪨 حجرة", callback_data="bot_r"),
            types.InlineKeyboardButton("📜 ورقة", callback_data="bot_p"),
            types.InlineKeyboardButton("✂️ مقص", callback_data="bot_s")
        )
        bot.reply_to(m, "🎮 **تحدي البوت الملكي**\nاختر سلاحك الآن:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(('bot_', 'pvp_')))
    def rps_callback(call):
        uid = call.from_user.id

        # --- نتائج اللعب ضد البوت ---
        if call.data.startswith('bot_'):
            user_choice = call.data.split('_')[1]
            bot_choice = random.choice(['r', 'p', 's'])
            
            if user_choice == bot_choice:
                res = "⚖️ تعادل!"
            elif (user_choice == 'r' and bot_choice == 's') or \
                 (user_choice == 'p' and bot_choice == 'r') or \
                 (user_choice == 's' and bot_choice == 'p'):
                res = "🎉 فزت عليّ! كفو."
                db_manager.update_user_gold(uid, 50) # جائزة الفوز
            else:
                res = "😎 هزمتك! حاول مرة أخرى."
            
            final_text = (
                f"👤 أنت: {choices_map[user_choice]}\n"
                f"🤖 أنا: {choices_map[bot_choice]}\n"
                f"━━━━━━━━━━━━\n"
                f"✨ النتيجة: {res}"
            )
            bot.edit_message_text(final_text, call.message.chat.id, call.message.message_id)

        # --- نتائج اللعب ضد صديق ---
        elif call.data.startswith('pvp_'):
            _, game_id, choice = call.data.split('_')
            if game_id not in pvp_games: return
            
            game = pvp_games[game_id]
            if uid == game['p1']: game['p1_choice'] = choice
            elif uid == game['p2']: game['p2_choice'] = choice
            else: return bot.answer_callback_query(call.id, "❌ لست طرفاً في هذا التحدي!")
            
            bot.answer_callback_query(call.id, "✅ تم تسجيل سلاحك!")

            if game['p1_choice'] and game['p2_choice']:
                c1, c2 = game['p1_choice'], game['p2_choice']
                winner_id = None
                
                if c1 == c2: res = "⚖️ تعادل ملكي!"
                elif (c1=='r' and c2=='s') or (c1=='p' and c2=='r') or (c1=='s' and c2=='p'):
                    res = f"👑 الفائز: {game['p1_name']}"
                    winner_id = game['p1']
                else:
                    res = f"👑 الفائز: {game['p2_name']}"
                    winner_id = game['p2']
                
                if winner_id:
                    db_manager.update_user_gold(winner_id, 50) # جائزة الفوز
                
                final_msg = (
                    f"🛡️ **نتيجة التحدي**\n"
                    f"━━━━━━━━━━━━\n"
                    f"👤 {game['p1_name']}: {choices_map[c1]}\n"
                    f"👤 {game['p2_name']}: {choices_map[c2]}\n"
                    f"━━━━━━━━━━━━\n"
                    f"✨ {res}\n"
                    f"💰 الجائزة: +50 ذهبة"
                )
                bot.edit_message_text(final_msg, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
                del pvp_games[game_id]
