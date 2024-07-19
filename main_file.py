import telebot
import requests
import random
import json
from TOKEN_API import TOKEN, OWM_API_KEY
from functions import exchange_rate_to_dollar

info_bot = telebot.TeleBot(TOKEN)

commands = [
    "start - начало работы",
    "course - вывод курса валют по отношению к доллару",
    "weather - состояние погоды в городе",
    "fact - рандомный факт"
]
str_commands = '\n'.join(commands)

facts = [
    "В течение 20 лет кот занимал пост мэра города на Аляске",
    "Вы с большей вероятностью подцепите компьютерный вирус, посещая религиозные сайты, чем сайты для взрослых",
    "Сладкую вату изобрел дантист",
    "Облако может весить более 450 тонн",
    "Шмели могут летать выше горы Эверест",
    "Плач делает вас счастливее",
    "Чайный пакетик был случайным изобретением",
    "Бумажные пакеты могут быть хуже для окружающей среды, чем пластиковые",
    "Большинство жителей Исландии верят в эльфов"
]

data = dict()

@info_bot.message_handler(commands=["start"])
def greetings(message):
    info_bot.reply_to(message, 'Приветствую тебя пользователь')
    with open("ID.json", 'w', encoding='utf-8') as f:
        ID = message.from_user.id
        NAME_USER = message.from_user.first_name
        data[ID] = [NAME_USER]
        json.dump(data, f, indent=4)

@info_bot.message_handler(commands=['course'])
def course_USD(message):
    command_text = message.text.split()
    
    if len(command_text) > 1:
        currency = command_text[1].upper()
        if currency in exchange_rate_to_dollar:
            rate = exchange_rate_to_dollar[currency]
            info_bot.reply_to(message, f'Курс {currency} к доллару: {rate}')
        else:
            info_bot.reply_to(message, 'Неизвестная валюта. Попробуйте другую.')
    else:
        info_bot.reply_to(message, 'Пожалуйста, укажите валюту после команды, например, /course.')

@info_bot.message_handler(commands=['weather'])
def send_weather(message):
    try:
        city = message.text.split()[1]
        weather = get_weather(city)
        info_bot.reply_to(message, weather)
    except IndexError:
        info_bot.reply_to(message, "Пожалуйста, укажите город после команды /weather")

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric&lang=ru'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        return (f"Погода в городе {city}:\n"
                f"Описание: {weather_description}\n"
                f"Температура: {temperature}°C\n"
                f"Ощущается как: {feels_like}°C\n"
                f"Влажность: {humidity}%\n"
                f"Скорость ветра: {wind_speed} м/с")
    else:
        return "Город не найден"
        
@info_bot.message_handler(commands=['help'])
def help_user(message):
    info_bot.reply_to(message, f"Команды бота:\n {str_commands}")
    
@info_bot.message_handler(commands=['fact'])
def trans_text(message):
    info_bot.reply_to(message, f"Факт: {facts[random.randint(0, len(facts))]}")
    
info_bot.polling()