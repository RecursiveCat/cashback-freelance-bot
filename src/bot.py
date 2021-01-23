from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import TeleBot 
from sql import Sql

class CashBackBot:
	def __init__(self, token):
		'''Подключаемся к базе данных и к БД'''
		self.sql = Sql()
		self.bot = TeleBot(token)
		self.nothing_button = InlineKeyboardButton(text = "❌", callback_data = "cancel")
		self.in_process = [] #переменная, для обозначения админов, которые настраивают бонусы, необходимая мера, чтобы избежать багов

	def start_command(self, message):
		'''Комманда /start'''
		if len(message.text.split()) > 1:
			refer = message.text.split()[1]
			if not self.sql.user_telegram_id_exists(message.from_user.id):
				self.sql.make_new_user(message.from_user.id, message.from_user.first_name + " " + message.from_user.last_name).commit()

		keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
		user_type = self.sql.get_user_type_by_id(message.from_user.id)
		if user_type == "customer":
			keyboard.row("Мои бонусы", "Реферальная программа")
			keyboard.row("Совершить покупку","О нас")

		elif user_type == "admin":
			keyboard.row("Начислить бонусы", "Списать бонусы")
			keyboard.row("Настроить бонусы", "Посмотреть базу")

		elif user_type == "operator":
			keyboard.row("Начислить бонусы", "Снять бонусы")


		self.bot.send_message("Здравствуйте, выберите пункт из списка:", reply_markup = keyboard)

	def customer_commands(self, message):
		'''Команды покупателя'''
		if message.text == "Мои бонусы":
			if self.sql.user_telegram_id_exists(message.from_user.id):
				if self.sql.get_user_type_by_id(message.from_user.id) == "customer":
					bonuses = self.sql.get_user_all_bonuses_by_id(message.from_user.id)
					keyboard = InlineKeyboardMarkup()
					keyboard.add(self.nothing_button)
					self.bot.send_message(message.chat.id, "Ваши бонусы: <b>{}</b>".format(bonuses), 
					reply_markup = keyboard, parse_mode = "HTML")

		elif message.text = "Реферальная программа":
			if self.sql.user_telegram_id_exists(message.from_user.id):
				if self.sql.get_user_type_by_id(message.from_user.id) == "customer":
					keyboard = InlineKeyboardMarkup()
					keyboard.add(self.nothing_button)
					link = "https://telegram.me/cashtestback_bot?start=" + str(message.from_user.id)
					self.bot.send_message(message.chat.id, 
						"""
						Рыба текст.
						Повседневная практика показывает, 
						что постоянное информационно-пропагандистское 
						обеспечение нашей деятельности влечет за собой процесс внедрения и модернизации дальнейших направлений развития. 
						<b>Ваша реферальная ссылка:</b> %s
						""" % link, parse_mode = "HTML" )

		elif message.text == "Совершить покупку":
			if self.sql.user_telegram_id_exists(message.from_user.id):
				if self.sql.get_user_type_by_id(message.from_user.id) == "customer":
					first_name = message.from_user.first_name
					last_name = str(message.from_user.last_name).replace("None", "")
					self.bot.send_message(message.chat.id, "Ожидайте, чтобы продавец с Вами связался...")
					for admin in admins:
						self.bot.send_message(admin, f"<b>{first_name} {last_name}</b> хочет произвести операцию.",
							parse_mode = "HTML")

		elif message.text == "О нас":
			self.bot.send_message("""
				Рыба текст
				 Повседневная практика показывает, 
				 что укрепление и развитие структуры обеспечивает широкому кругу (специалистов) участие в формировании дальнейших направлений развития. 
				 Разнообразный и богатый опыт укрепление и развитие структуры способствует подготовки и реализации позиций, занимаемых участн
				 Значимость этих проблем настолько очевидна, что постоянное информационно-пропагандистское условий. 
				""")

	def admin_commands(self, content_type, query):
		if content_type == "message":
			message = query 
			if message.text == "Настроить бонусы":
				if self.sql.user_telegram_id_exists(message.from_user.id):
					if self.sql.get_user_type_by_id(message.from_user.id) == "admin":
						keyboard = InlineKeyboardMarkup()
						button_referal = InlineKeyboardButton(text = "Реферал", callback_data=f"config_referal_{message.from_user.id}")
						button_bonus = InlineKeyboardButton(text = "Бонус", callback_data=f"config_bonus_{message.from_user.id}")
						keyboard.add(button_bonus, button_referal)
						keyboard.add(self.nothing_button)
						self.bot.send_message(message.chat.id, "Что вы хотите настроить?", reply_markup = keyboard)

					elif self.sql.get_user_type_by_id(message.from_user.id) in ("admin", "operator"):
						if message.text == "Начислить бонусы":
							self.bot.send_message(message.chat.id, "Введите код: ")

						elif mesage.text == "Списать бонусы":
							pass


		elif content_type == "call":
			call = query
			if call.data.startswith("config"):
				need_data = call.data.split("_")
				param = need_data[1]
				user = need_data[2]
				self.bot_send_message(call.message.chat.id, "Введите число от 1>100%")
				self.in_process.add({"user":int(user), "move": f"config_{param}"})




