import telebot
from telebot import types
import random
import db_manager

def register_handlers(bot):
    games = {}

    @bot.message_handler(func=lambda m: m.text in ["اكس او", "اكس", "xo"])
    def start_xo(m):
        uid = m.from_user.id
        msg = (
            "━━━━━━━━━━━━━━━━\n"
            "   🕹️ **تحدي إكس أو (XO)**\n"
            "━━━━━━━━━━━━━━━━\n"
            "• أول شخص يضغط على 'بدء التحدي' سيلعب معك.\n"
            "• أو اضغط 'لعب ضد البوت' للممارسة.\n"
            "━━━━━━━━━━━━━━━━"
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("🤝 بدء التحدي", callback_data=f"xo_join_{uid}"),
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
            games[p1_id] = {"board": [" "] * 9, "p1": p1_id, "p2": "bot", "turn": p1_id}
            render_board(bot, call.message, p1_id)

        # --- انضمام صديق للتحدي ---
        elif action == "join":
            p2_id = call.from_user.id
            if p2_id == p1_id:
                bot.answer_callback_query(call.id, "لا يمكنك تحدي نفسك يا ملك!")
                return
            games[p1_id] = {"board": [" "] * 9, "p1": p1_id, "p2": p2_id, "turn": p1_id}
            render_board(bot, call.message, p1_id)

        # --- الضغط على المربعات ---
        elif action == "move":
            idx = int(data[3])
            game_id = p1_id
            if game_id not in games: return
            
            game = games[game_id]
            if call.from_user.id != game["turn"]: return
            
            symbol = "X" if call.from_user.id == game["p1"] else "O"
            if game["board"][idx] == " ":
                game["board"][idx] = symbol
                
                if check_win(game["board"], symbol):
                    end_game(bot, call.message, game, f"الفائز هو: {call.from_user.first_name} ✨")
                elif " " not in game["board"]:
                    end_game(bot, call.message, game, "تعادل ملكي! 🤝")
                else:
                    # تبديل الدور
                    if game["p2"] == "bot":
                        bot_move(game)
                        if check_win(game["board"], "O"):
                            end_game(bot, call.message, game, "فاز البوت! حظاً أوفر.")
                        elif " " not in game["board"]:
                            end_game(bot, call.message, game, "تعادل!")
                        else:
                            render_board(bot, call.message, game_id)
                    else:
                        game["turn"] = game["p2"] if game["turn"] == game["p1"] else game["p1"]
                        render_board(bot, call.message, game_id)

    def bot_move(game):
        empty_cells = [i for i, v in enumerate(game["board"]) if v == " "]
        if empty_cells:
            idx = random.choice(empty_cells)
            game["board"][idx] = "O"

    def check_win(b, s):
        win_states = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(b[i]==b[j]==b[k]==s for i,j,k in win_states)

    def render_board(bot, message, game_id):
        game = games[game_id]
        markup = types.InlineKeyboardMarkup()
        btns = []
        for i in range(9):
            txt = game["board"][i] if game["board"][i] != " " else str(i+1)
            btns.append(types.InlineKeyboardButton(txt, callback_data=f"xo_move_{game_id}_{i}"))
        
        markup.add(*btns[0:3])
        markup.add(*btns[3:6])
        markup.add(*btns[6:9])
        
        turn_name = "دورك الآن" if game["p2"] == "bot" else f"دور: {bot.get_chat_member(message.chat.id, game['turn']).user.first_name}"
        bot.edit_message_text(f"🎮 **تحدي XO قـائم**\n━━━━━━━━━━━━\n{turn_name}", 
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
