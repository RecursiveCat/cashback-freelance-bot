from keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot


class CashbackBot:
	def __init__(self, token):
		'''Подключение к Telegram, SQL'''
		self.bot = TeleBot(token)
		'''это кнопка отмены, она часто используется, поэтому я добавил ее в переменные класса'''
		self.button_cancel = InlineKeyboardButton(text = "❌", callback_data = "cancel")

		'''переменная для обозначения предпринимателей, которые находятся в процессе настройки процентов'''
		self.users_in_process = []

	def start_command(self, query, is_callback_query=False):
		if not is_callback_query:
			message = query
			if not self.id_exists_in_table("id",message.from_user.id,"users"):
				if " " in message.text:
					ref_data = message.text.split()[1]
					if ref_data[0] == "o":
						ref_data = ref_data.split("o")[1]
						inst_id = int(ref_data)
						inst_name = self.sql.get_institution_info_by_id(inst_id)['institution_name']
						self.bot.send_message(user_id, parse_mode = "HTML",
							text = f"Теперь вы оператор <b>{inst_name}</b>!")
						self.bot.send_message(message.chat.id, "Оператор приглашен.")
						# тут нужен sql	
					elif ref_data[0] == "u"
						ref_data = ref_data.split("u")
						inst_id = int(ref_data[1])
						user_id = int(ref_data[0])
						inst_name = self.sql.get_institution_info_by_id(inst_id)['institution_name']
						self.bot.send_message(user_id, parse_mode = "HTML",
							text = f"У вас новый реферал на предприятие <b>{inst_name}</b>!\n Имя реферала:<b>{user_name}</b>")
						self.bot.send_message(message.chat.id, f"Вы были приглашены по реферальной ссылке к предприятию <b>{inst_name}</b>",
							parse_mode = "HTML")
						# тут нужен sql
				self.sql.create_user_as(message.from_user.id, message.from_user.first_name + " " + message.from_user.last_name, "customer")

			keyboard = InlineKeyboardMarkup()
			button_buy = InlineKeyboardButton(text = "Совершить покупку", callback_data = "menu|buy")
			button_referal = InlineKeyboardButton(text = "Реферальная программа", callback_data = "menu|refer")
			button_about = InlineKeyboardButton(text = "О боте", callback_data = "menu|about")
			keyboad.add(button_buy, button_referal)
			keyboard.add(button_about, self.button_cancel)
			self.bot.send_message(message.chat.id, f"Здравствуйте <b>{message.from_user.first_name}</b>", 
				parse_mode = "HTML", reply_markup = keyboard)
		else:
			call = query
			if call.data.startswith("menu"):
				menu_type = call.data.split("|")[1]

				if menu_type == "buy":
					keyboard = InlineKeyboardMarkup()
					button_bonus_plus = InlineKeyboardButton(text = "Начислить", callback_data = "bonus|plus")
					button_bonus_mins = InlineKeyboardButton(text = "Списать", callback_data = "bonus|mins")
					keyboard.add(button_bonus_plus, button_bonus_mins)
					keyboard.add(self.button_cancel)
					self.bot.edit_message_text(chat_id = call.message.chat.id, text = "Что вы намерены делать с бонусами?", 
						reply_markup = keyboard, message_id = call.message.message_id)

				elif menu_type == "refer":
					insts = #тут нужен sql #self.sql.get_insts(call.from_user.id)
					if insts == []:
						self.bot.send_message(call.message.chat.id, "Вы не работали ни с какими предприятиями 🚫")
					else:
						keyboard = InlineKeyboardMarkup()
						for inst in insts:
							name = self.sql.get_institution_info_by_id(inst)["institution_name"]
							keyboard.add(InlineKeyboardButton(text=name,callback_data=f"refer|{inst}"))
						keyboard.add(self.button_cancel)
						self.bot.edit_message_text(chat_id = call.message.chat.id, 
							text = "Выберите предприятие, к которому вы хотите получить реферальную ссылку:",
							reply_markup = keyboard, message_id = call.message.message_id)

				elif menu_type == "about":
					self.bot.send_message(call.message.chat.id, 
						"""
						Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
						Sed vitae ornare elit. Morbi pellentesque bibendum leo quis hendrerit. 
						Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
						""")


			elif call.data.startswith("refer"):
				inst_id = call.data.split("|")[1]
				link = f"http://t.me/cashtestback_bot?start=u{call.from_user.id}q{inst_id}"
				self.bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,
					text = f"Используйте эту ссылку, чтобы пригласить нового пользователя\n{link}")


			elif call.data.startswith("bonus"):
				need_data = call.data.split("|")
				bonus_type = need_data[1]

				operation_id = self.sql.gen_random_id() 
				#тут нужен sql

				self.bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,
					text = f"Ваш код: <b>{operation_id}</b>\nСообщите этот код кассиру.")

	def admin_commands(self, query, is_callback_query=False):
		if not is_callback_query:
			message = query
			if self.sql.check_user(message.from_user.id):
				keyboard = InlineKeyboardMarkup()
				button_settings = InlineKeyboardButton(text = "Настройки", callback_data = "settings")
				button_add_operator = InlineKeyboardButton(text = "Добавить оператора", callback_data = "add_operator")
				button_buy = InlineKeyboardButton(text = "Совершить продажу", callback_data = "buy")
				keyboard.add(button_settings, button_add_operator)
				keyboard.add(button_buy, self.button_cancel)
				self.bot.send_message(message.chat.id,"Меню предприятия:",reply_markup=keyboard)

			elif message.from_user.id in [process.get("user_id") for process in self.users_in_process]:
				for process in self.users_in_process:
					if process.get("user_id") == message.from_user.id:
						theme = process.get("item")
						break
				theme_text = theme.replace("referal","рефералов").replace("reffer","рефферов").replace("bounus","бонусов")

				if item.startswith("buy"):
					if item == "buy":
						if not in #тут sql:
							self.bot.send_message(message.chat.id, "Данный код не найден, попробуйте ввести снова или ввести <b>Отмена</b> для отмены",
								parse_mode = "HTML")
						else:
							self.bot.send_message(message.chat.id, "Введите сумму покупки: ")
							self.users_in_process.remove(process)
							self.users_in_process.append({"user_id":message.from_user.id, "item":"buy2", "code":message.text})
					else:
						try:
							count = int(message.text)
							inst_id = #тут нужен sql #self.sql.get_inst_id(message.from_user.id)
							do = #тут нужн sql # self.sql.get_do(process['code'])
							self.sql.bonuses_to_user(self,user_id,count,inst_id,do)
							referals = #тут нужен sql
							percent_for_referal = #тут нужен sql
							sale = referals * percent_for_referal
							count = count / 100 * sale
							self.bot.send_message(message.chat.id, parse_mode = "HTML",
								text = f"Операция прошла успешно! Сумма покупки равна: <b>{count}</b>, так как <b>{referals}</b> реферал")
							self.users_in_process.remove(process)
													
						except ValueError:
							self.bot.send_message(message.chat.id, "Вы ввели не по формату, попробуйте еще раз или введите <b>Отмена</b>",
								parse_mode = "HTML")

				
				if message.text == "Отмена":
					self.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
					self.users_in_process.remove(process)


				elif message.text not in [str(i) for i in range(1,101)]:
					self.bot.send_message(message.chat.id, "Вы ввели не по формату, попробуйте еще раз или введите <b>Отмена</b>",
						parse_mode = "HTML")

				else:
					self.bot.send_message(message.chat.id, f"Ваш новый процент для <b>{theme_text}</b> -- <b>{message.text}%</b>",
						parse_mode = "HTML")
					#тут нужен sql


		else:
			call = query
			if call.data == "add_operator":
				inst_id = #тут нужен sql #self.sql.get_inst(call.from_user.id)
				link = f"http://t.me/cashtestback_bot?start=o{inst_id}"
				self.bot.send_message(call.message.chat.id, f"Используйте эту ссылку, чтобы добавить в ваше предприятие оператора:\n{link}")

			elif call.data == "settings":
				keyboard = InlineKeyboardMarkup()
				button_referal = InlineKeyboardButton(text = "Проценты на рефералы", callback_data = "config|referal")
				button_reffer = InlineKeyboardButton(text = "Проценты на рефферы", callback_data = "config|reffer")
				button_bonus = InlineKeyboardButton(text = "Бонусы", callback_data = "config|bonus")
				keyboard.add(button_referal, button_reffer)
				keyboard.add(button_bonus, self.button_cancel)
				self.bot.send_message(call.message.chat.id, "Настроить:", reply_markup = keyboard)

			elif call.data == "buy":
				self.users_in_process.append({"user_id":call.from_user.id, "item":"buy"})
				self.bot.send_message(call.message.chat.id, "Введите код: ")


			elif call.data.startswith("config"):
				item = call.data.split("|")[1]
				self.bot.send_message(call.message.chat.id, "Введите число от 1>100")
				self.users_in_process.append({"user_id":call.from_user.id, "item":item})


