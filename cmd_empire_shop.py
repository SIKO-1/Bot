def register_shop_handlers(bot):
    
    @bot.message_handler(func=lambda m: m.text in ["متجر", "المتجر"])
    def empire_shop(m):
        bot.reply_to(m, "👑 تم تفعيل متجر الإمبراطورية الجديد بنجاح!")
