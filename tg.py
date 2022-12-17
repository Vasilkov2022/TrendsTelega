import telebot
from telebot import types
from tinydb import TinyDB
from weatherbit.api import Api


db = TinyDB('tinydb.json')
apiToken = '1b3d4575b5de40e1bb35967cd7ea97f3'

api = Api(apiToken)
api.set_granularity('daily')
token = '5905366611:AAEeeOK7F1HCJWHKGm8iExJdpPs8p4wRGv4'
bot = telebot.TeleBot(token, parse_mode=None)

def higher_temp(city):
    forecast = api.get_forecast(city=city, hours=1)
    res = forecast.get_series(['high_temp','low_temp','weather'])
    return res[0]['high_temp']


def lower_temp(city):
    forecast = api.get_forecast(city=city, hours=1)
    res = forecast.get_series(['high_temp', 'low_temp', 'weather'])
    return res[0]['low_temp']

def weather(city):
    forecast = api.get_forecast(city=city, hours=1)
    res = forecast.get_series(['high_temp', 'low_temp', 'weather'])
    return res

def descript(city):
    forecast = api.get_forecast(city=city, hours=1)
    return forecast.get_series(['weather'])[0].get('weather').get('description')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    regbt1 = types.KeyboardButton('Санкт-Петербург')
    regbt2 = types.KeyboardButton('Москва')
    regbt3 = types.KeyboardButton('Самара')
    regbt4 = types.KeyboardButton('Новый Урегной')
    otherbt = types.KeyboardButton('Другой город')
    markup.add(regbt1, regbt2, regbt3, regbt4, otherbt)
    bot.send_message(message.chat.id, "Выберите регион:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def btn_handler(message):
    if message.text != 'Другой город':
        try:
            bot.send_message(message.chat.id, 'Погода сегодня:')
            bot.send_message(message.chat.id, 'Самая высокая температура:' + ' ' + str(higher_temp(message.text)) + "ºC")
            bot.send_message(message.chat.id, 'Самая низкая температура:' + " " + str(lower_temp(message.text)) + "ºC")
            bot.send_message(message.chat.id, 'Описание:' + ' ' + str(descript(message.text)))
        except:
            bot.send_message(message.chat.id, 'В данный момент погода недоступна для вашего региона, или создатель должен купить подписку за 8$')
    else:
        bot.send_message(message.chat.id, 'Напишите название горрода')
        # bot.send_message(message.chat.id, 'Погода сегодня:')
        # bot.send_message(message.chat.id, 'Самая высокая температура:' + str(higher_temp('Moscow')))

        # if message.text == 'Санкт-Петербург':
        #     bot.send_message(message.chat.id, "Погода в этом часу:")
        #     bot.send_message(message.chat.id, 'Самая высокая температура:' + str(higher_temp('Saint Petersburg')))
        # if message.text == "Москва":
        #     bot.send_message(message.chat.id, "Погода в этом часу:")
        #     bot.send_message(message.chat.id, 'Самая высокая температура:' + str(higher_temp(message.text)))


bot.infinity_polling()
