import telegram

TOKEN = '7350497618:AAFQZgTZamkI3-k_93LdHvxTzCYl1sjp_ns'
bot = telegram.Bot(token=TOKEN)

updates = bot.get_updates()
# print(updates)
# print(updates[0]['my_chat_member']['chat']['id'])