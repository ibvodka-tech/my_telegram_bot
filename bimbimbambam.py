import telebot

token = '8842032480:AAG7FnNW3SowJGd9hnjiEss_n5-xhqzKGbQ'
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, message.text)

bot.infinity_polling()    