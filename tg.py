import telebot
from telebot import types
from tinydb import TinyDB
from weatherbit.api import Api


db = TinyDB('tinydb.json')
apiToken = '1b3d4575b5de40e1bb35967cd7ea97f3'

api = Api(apiToken)
api.set_granularity('daily')
token = '5747802076:AAEiCodUJQv0thfDQ4GO4BBTsa1EGVMpYx4'
bot = telebot.TeleBot(token, parse_mode=None)

def higher_temp(city):
    forecast = api.get_forecast(city=city, hours=1)
    res =  forecast.get_series(['high_temp','low_temp','weather'])
    return res[0]['high_temp']
print(higher_temp('Moscow'))

def lower_temp(city):
    forecast = api.get_forecast(city=city, hours=1)
    res = forecast.get_series(['high_temp', 'low_temp', 'weather'])
    return res[0]['low_temp']
print(lower_temp('Woscow'))

def weather(city):
    forecast = api.get_forecast(city=city, hours=1)
    res = forecast.get_series(['high_temp', 'low_temp', 'weather'])
    return res
print(weather('Woscow'))

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    regbt1 = types.KeyboardButton('Санкт-Петербург')
    regbt2 = types.KeyboardButton('Москва')
    regbt3 = types.KeyboardButton('Самара')
    markup.add(regbt1, regbt2, regbt3)
    db.insert({message.chat.username: message.chat.id})
    bot.send_message(message.chat.id, "Выберите регион:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def btn_handler(message):
    if message.text == 'Санкт-Петербург':
        bot.send_message(message.chat.id, "Погода в этом часу:")
        bot.send_message(message.chat.id, 'Самая высокая температура:' + str(higher_temp('Saint Petersburg')))
    if message.text == "Москва":
        bot.send_message(message.chat.id, "Погода в этом часу:")
        bot.send_message(message.chat.id, 'Самая высокая температура:' + str(higher_temp('Москва')))

bot.infinity_polling()
