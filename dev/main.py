from telebot import telebot
from bot import CashbackBot
import config

bot = TeleBot(config.token)

cmd = CashbackBot(config.token)

@bot.message_handler(commands=['start'])
def any_start(message):
	cmd.start_command(message, False)

@bot.message_handler(commands=['admin'])
def any_admin(message):
	cmd.admin_commands(message, False)

@bot.message_handler(content_types=['text'])
def any_text(message):
	cmd.start_command(message, False)
	cmd.admin_commands(message, False)

@bot.callback_query_handler(lambda call: True)
def any_call(call):
	cmd.start_command(call, True)
	cmd.admin_commands(call, True)

bot.polling(none_stop = True)