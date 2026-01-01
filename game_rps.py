import random
from telebot import types

def register_handlers(bot):
    
    pvp_games = {}
    choices_map = {'r': '🪨', 'p': '📜', 's': '✂️'}

    @bot.message_handler(func=lambda m: m.text.split()[0] in ['حجره', 'حجرة', 'مقص', 'ورقة', 'ورقه', 'حجر'])
    def start_rps(m):
        chat_id = m.chat.id
        user_id = m.from_user.id
        args = m.text.split()
        
        # --- نظام اللعب ضد صديق ---
        if m.reply_to_message or len(args) > 1:
            opponent = m.reply_to_message.from_user if m.reply_to_message else None
            if opponent:
                if opponent.id == bot.get_me().id:
                    bot.reply_to(m, "⚠️ العب معي بدون تاك!")
                    return
                
                game_id = f"{user_id}_{opponent.id}_{m.message_id}"
                pvp_games[game_id] = {
                    "p1": user_id, "p2": opponent.id,
                    "p1_choice": None, "p2_choice": None,
                    "p1_name": m.from_user.first_name, "p2_name": opponent.first_name
                }
                
                markup = types.InlineKeyboardMarkup()
                markup.row(
                    types.InlineKeyboardButton("🪨 حجرة", callback_data=f"pvp_{game_id}_r"),
                    types.InlineKeyboardButton("📜 ورقة", callback_data=f"pvp_{game_id}_p"),
                    types.InlineKeyboardButton("✂️ مقص", callback_data=f"pvp_{game_id}_s")
                )
                bot.send_message(chat_id, f"⚔️ **تحدي الإمبراطورية بدأ!**\n\n{m.from_user.first_name} 🆚 {opponent.first_name}\n\n📥 اختارا سلاحكما الآن..", reply_markup=markup)
                return

        # --- نظام اللعب ضد البوت ---
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("🪨 حجرة", callback_data="bot_r"),
            types.InlineKeyboardButton("📜 ورقة", callback_data="bot_p"),
            types.InlineKeyboardButton("✂️ مقص", callback_data="bot_s")
        )
        bot.reply_to(m, "🎮 **اختر سلاحك { حجره - ورقه - مقص }**", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(('bot_', 'pvp_')))
    def rps_callback(call):
        # --- نتائج اللعب ضد البوت ---
        if call.data.startswith('bot_'):
            user_choice = call.data.split('_')[1]
            bot_choice = random.choice(['r', 'p', 's'])
            
            if user_choice == bot_choice:
                res = "تعادل"
            elif (user_choice == 'r' and bot_choice == 's') or \
                 (user_choice == 'p' and bot_choice == 'r') or \
                 (user_choice == 's' and bot_choice == 'p'):
                res = "فوزك!"
            else:
                res = "خسارتك.."
            
            final_text = (
                f"💥| انت : {choices_map[user_choice]}\n"
                f"💥| انا : {choices_map[bot_choice]}\n"
                f"〽| النتيجه : {res}"
            )
            bot.edit_message_text(final_text, call.message.chat.id, call.message.message_id)

        # --- نتائج اللعب ضد صديق ---
        elif call.data.startswith('pvp_'):
            _, game_id, choice = call.data.split('_')
            if game_id not in pvp_games: return
            
            game = pvp_games[game_id]
            if call.from_user.id == game['p1']: game['p1_choice'] = choice
            elif call.from_user.id == game['p2']: game['p2_choice'] = choice
            
            bot.answer_callback_query(call.id, "✅ تم تسجيل اختيارك!")

            if game['p1_choice'] and game['p2_choice']:
                c1, c2 = game['p1_choice'], game['p2_choice']
                
                if c1 == c2: res = "تعادل"
                elif (c1=='r' and c2=='s') or (c1=='p' and c2=='r') or (c1=='s' and c2=='p'):
                    res = f"فوز {game['p1_name']}"
                else:
                    res = f"فوز {game['p2_name']}"
                
                final_msg = (
                    f"💥| {game['p1_name']} : {choices_map[c1]}\n"
                    f"💥| {game['p2_name']} : {choices_map[c2]}\n"
                    f"〽| النتيجه : {res}"
                )
                bot.edit_message_text(final_msg, call.message.chat.id, call.message.message_id)
                del pvp_games[game_id]
