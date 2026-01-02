def register_shop_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text in ["متجر", "المتجر", "شوب", "shop"])
    def send_welcome_shop(m):
        bot.reply_to(m, "اهلا بك في المتجر")
