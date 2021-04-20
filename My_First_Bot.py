import telebot
import datetime
from telebot import types
import requests
import datetime
import schedule
import threading
import time

today = datetime.datetime.today()
date = today.strftime("%Y-%m-%d")

API_TOKEN = '1731631692:AAFZjOqzeQHcFmVFtNGLSPLnYg4gaR5qpng'
bot = telebot.TeleBot(API_TOKEN)

time1 = str(datetime.date.today()).replace('-', '')


class Exchange():
    val = "USD"
    date = time1

    def __init__(self, v, d):
        if not isinstance(v, str):
            raise TypeError
        if len(v) != 3:
            raise TypeError
        if len(d) != 8:
            raise TypeError
        try:
            d = int(d)
            d = d
        except:
            raise TypeError
        self.val, self.date = v, d


def Api_get():
    try:
        curs = requests.get(f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json?\
        valcode={Exchange.val}&date={Exchange.date}')
        curs = curs.json()
        return curs
    except:
        raise ConnectionError

def USD():
    cur = Api_get()
    vl = Exchange.val
    my_list = []
    for x in cur:
        if x['cc'] == vl:
            my_list.append(f"{x['txt']} to UAH: -> {x['rate']}")
    return my_list

def EUR():
    Exchange.val = 'EUR'
    cur = Api_get()
    vl = Exchange.val
    my_list = []
    for x in cur:
        if x['cc'] == vl:
            my_list.append(f"{x['txt']} to UAH: -> {x['rate']}")
    return my_list

dollar = str(*USD())
euro = str(*EUR())


def bitkoin():
    try:
        bit = requests.get('https://apirone.com/api/v1/ticker?currency=btc')
        bit = bit.json()
        return str(bit['UAH'])
    except:
        raise ConnectionError


bitok = bitkoin()
bitok = f'Биткоин to UAH: -> {bitok[9:-1]}'


def corona():
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"

    querystring = {"country":"Ukraine"}

    headers = {
        'x-rapidapi-key': "5ec2d02cc7msh54c3cc16fe5e816p1febb1jsn0389c3229510",
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()

    stat = response['data']
    stat1 = stat['covid19Stats']
    odessa = stat1[16]
    statistic = [value for key, value in odessa.items()]
    statistic = statistic[5:]
    finish = f'Дата {date}\nСтатистика за все время\nОдесская Область\nПодтвержденный у {statistic[0]} человек \nУмерло {statistic[1]} человек \nВыздоровели {statistic[2]} человек'
    return finish

coronaV = str(corona())


@bot.message_handler(commands=['start'])
def start_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('USD', 'EUR', 'Bitcoin', 'COVID Statistic')
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def end_text(message):
    if message.text.lower().strip() == 'привет':
        bot.send_message(message.chat.id, 'Привет')
    if message.text.lower().strip() == 'usd':
        bot.send_message(message.chat.id, dollar)
    if message.text.lower().strip() == 'bitcoin':
        bot.send_message(message.chat.id, bitok)
    if message.text == 'COVID Statistic':
        bot.send_message(message.chat.id, coronaV)
    if message.text.lower().strip() == 'eur':
        bot.send_message(message.chat.id, euro)
    elif message.text.lower().strip() == 'пока':
        bot.send_message(message.chat.id, 'До свидания')
    elif message.text.lower().strip() == 'покажись':
        my_photo = open(r'1.jpg', 'rb')
        bot.send_photo(message.chat.id, my_photo)

bot.polling()
