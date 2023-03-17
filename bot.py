import telebot
import requests
import json

from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

seat = ''
carriage = ''
date = ''
TOKEN = json.load(open('env.json'))['access_key']

bot = telebot.TeleBot(TOKEN)
bot.set_webhook()

@bot.message_handler(commands=["block"])
def set_carriage(message, res=False):
	bot.send_message(message.chat.id, 'Напиши номер вагона')
	bot.register_next_step_handler(message, set_seat);

def set_seat(message):
	global carriage;
	carriage = message.text;
	bot.send_message(message.chat.id, 'Напиши номер места');
	bot.register_next_step_handler(message, set_date, message.text);

def set_date(message, carriage):
	global seat;
	seat = message.text;
	calendar, step = DetailedTelegramCalendar().build();
	bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar);

# callback for calendar
@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
	result, key, step = DetailedTelegramCalendar().process(c.data)
	if not result and key:
		bot.edit_message_text(f"Select {LSTEP[step]}", c.message.chat.id, c.message.message_id, reply_markup=key)
	elif result:
		global date;
		date = result;
		bot.edit_message_text(f"Вагон: {carriage}, Место: {seat}, Дата: {date}", c.message.chat.id, c.message.message_id)
		send_request(c.message)

def send_request(message):
	bot.send_message(message.chat.id, "Тут отправляется запрос");

bot.polling(none_stop=True, interval=0)