import telebot
from telebot import types
import random
import db_manager # الربط بالخزنة الملكية

def register_handlers(bot):
    games = {}

    @bot.message_handler(func=lambda m: m.text in ["اكس او", "اكس", "xo"])
    def start_xo(m):
        uid = m.from_user.id
        name = m.from_user.first_name
        msg = (
            f"🕹️ **تحدي إكس أو (XO) الملكي**\n"
            f"━━━━━━━━━━━━━\n"
            f"👤 المبتدئ: [{name}](tg://user?id={uid})\n"
            f"💰 الجائزة: 100 ذهبة\n"
            f"━━━━━━━━━━━━━\n"
            f"بانتظار المنافس.. أو العب ضد البوت!"
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("🤝 قبول التحدي", callback_data=f"xo_join_{uid}"),
            types.InlineKeyboardButton("🤖 ضد البوت", callback_data=f"xo_bot_{uid}")
        )
        bot.reply_to(m, msg, reply_markup=markup, parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("xo_"))
    def handle_xo(call):
        data = call.data.split("_")
        action = data[1]
        p1_id = int(data[2])
        
        # --- بدء اللعب ضد البوت ---
        if action == "bot":
            if call.from_user.id != p1_id: return
            games[p1_id] = {"board": ["⬜"] * 9, "p1": p1_id, "p1_n": call.from_user.first_name, "p2": "bot", "p2_n": "🤖 البوت", "turn": p1_id}
            render_board(bot, call.message, p1_id)

        # --- انضمام صديق للتحدي ---
        elif action == "join":
            p2_id = call.from_user.id
            if p2_id == p1_id:
                return bot.answer_callback_query(call.id, "لا يمكنك تحدي نفسك!")
            
            games[p1_id] = {"board": ["⬜"] * 9, "p1": p1_id, "p1_n": "Player 1", "p2": p2_id, "p2_n": call.from_user.first_name, "turn": p1_id}
            # جلب الاسم الأول لصاحب التحدي
            try:
                p1_info = bot.get_chat_member(call.message.chat.id, p1_id)
                games[p1_id]["p1_n"] = p1_info.user.first_name
            except: pass
            
            render_board(bot, call.message, p1_id)

        # --- الضغط على المربعات ---
        elif action == "move":
            idx = int(data[3])
            game_id = p1_id
            if game_id not in games: return
            
            game = games[game_id]
            if call.from_user.id != game["turn"]: 
                return bot.answer_callback_query(call.id, "ليس دورك الآن! ⏳")
            
            symbol = "🟦" if call.from_user.id == game["p1"] else "🟥"
            if game["board"][idx] == "⬜":
                game["board"][idx] = symbol
                
                if check_win(game["board"], symbol):
                    winner_id = call.from_user.id
                    db_manager.update_user_gold(winner_id, 100) # إضافة الجائزة
                    end_game(bot, call.message, game, f"🎉 الفائز: {call.from_user.first_name}\n💰 ربح 100 ذهبة!")
                    del games[game_id]
                elif "⬜" not in game["board"]:
                    end_game(bot, call.message, game, "🤝 تعادل ملكي! لا يوجد رابح.")
                    del games[game_id]
                else:
                    if game["p2"] == "bot":
                        bot_move(game)
                        if check_win(game["board"], "🟥"):
                            end_game(bot, call.message, game, "💀 هزمك البوت! حاول مرة أخرى.")
                            del games[game_id]
                        elif "⬜" not in game["board"]:
                            end_game(bot, call.message, game, "🤝 تعادل!")
                            del games[game_id]
                        else:
                            render_board(bot, call.message, game_id)
                    else:
                        game["turn"] = game["p2"] if game["turn"] == game["p1"] else game["p1"]
                        render_board(bot, call.message, game_id)

    def bot_move(game):
        empty_cells = [i for i, v in enumerate(game["board"]) if v == "⬜"]
        if empty_cells:
            idx = random.choice(empty_cells)
            game["board"][idx] = "🟥"

    def check_win(b, s):
        win_states = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(b[i]==b[j]==b[k]==s for i,j,k in win_states)

    def render_board(bot, message, game_id):
        game = games[game_id]
        markup = types.InlineKeyboardMarkup()
        btns = [types.InlineKeyboardButton(game["board"][i], callback_data=f"xo_move_{game_id}_{i}") for i in range(9)]
        
        markup.add(*btns[0:3])
        markup.add(*btns[3:6])
        markup.add(*btns[6:9])
        
        curr_name = game["p1_n"] if game["turn"] == game["p1"] else game["p2_n"]
        bot.edit_message_text(f"🎮 **تحدي XO قـائم**\n━━━━━━━━━━━━\n🟦: {game['p1_n']}\n🟥: {game['p2_n']}\n━━━━━━━━━━━━\n📍 الدور الآن: **{curr_name}**", 
                             chat_id=message.chat.id, message_id=message.message_id, 
                             reply_markup=markup, parse_mode="Markdown")

    def end_game(bot, message, game, result):
        markup = types.InlineKeyboardMarkup()
        btns = [types.InlineKeyboardButton(v, callback_data="none") for v in game["board"]]
        markup.add(*btns[0:3])
        markup.add(*btns[3:6])
        markup.add(*btns[6:9])
        bot.edit_message_text(f"🏁 **انتهت اللعبة**\n━━━━━━━━━━━━\n{result}", 
                             chat_id=message.chat.id, message_id=message.message_id, 
                             reply_markup=markup, parse_mode="Markdown")
