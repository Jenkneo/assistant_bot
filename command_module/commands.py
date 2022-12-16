import os
import sys
import requests
import json
import re

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from config import DEBUG

def weather(user_input):
    # Функция для получения города из строки
    # Основой для поиска города является файл cities.json
    def get_city(string):
        with open("command_module/cities_list.json", encoding='utf8') as list_file:
            cities_list = json.loads(list_file.read())
            for city in cities_list.keys():
                for city_opt in cities_list[city]:
                    if city_opt in string:
                        return [city, cities_list[city][1]]
            return "Not found"

    # Функция заменяет первое число в строке
    # Основой для замены чисел является файл numbers.json
    def replace_number(string):
        number_in_string = re.findall('[0-9]+', string)[0]
        with open("command_module/numbers.json", encoding='utf8') as list_file:
            numbers_list = json.loads(list_file.read())
            try:
                return string.replace(str(number_in_string), numbers_list[number_in_string])
            except:
                return string

    def temperature_prettifyer(temperature):
        temperatures = re.findall('[0-9]+', temperature)
        print(temperatures)
        if len(temperatures) != 1:
            temperature = temperature.replace("(", "")
            temperature = temperature.replace(")", "")
            temperature = temperature.replace(str(temperatures[1]), "")
        temperature = temperature.replace("-", "минус ")
        temperature = temperature.replace("+", "плюс ")
        temperature = temperature.replace("°", "градусов ")
        temperature = temperature.replace("C", "")
        return temperature

    city = get_city(user_input)
    if city == "Not found":
        url = 'http://wttr.in/'
    else:
        url = 'http://wttr.in/' + city[0]
    parameters = {
        'format': '',
        '0': '',
        'T': '',
        'lang': 'ru',
        'M': '',
        'n': ''
    }

    try:
        response = requests.get(url, params=parameters)
    except requests.ConnectionError:
        return 'Извините, но произошла сетевая ошибка. Хотя мне кажется что я просто не подключена к интернету.'
    if response.status_code == 200:
        city_weather = response.text.split("\n")
        temperature = replace_number(temperature_prettifyer(city_weather[3][16:]))
        type_weather = city_weather[2][16:]
        if type_weather == "Light rain and hail with thunderstorm": type_weather = "небольшой дождь и град с грозой"
        print(response.text)
        if url == 'http://wttr.in/':
            return f"В вашем городе сейчас {type_weather}, {temperature}"
        else:
            return f"Сейчас в {city[1]} {type_weather}, {temperature}"
    else:
        return 'Извините, но произошла сетевая ошибка. Сервер погоды не отвечает.'

def command_open(user_input):
    with open("command_module/sites.json", encoding='utf8') as list_file:
        sites_list = json.loads(list_file.read())
        for site in sites_list.keys():
            for ru_site_name in sites_list[site]["ru_name"]:
                if ru_site_name in user_input:
                    os.system("start " + sites_list[site]["url"])
                    return "Слушаюсь!"

    with open("command_module/programms.json", encoding='utf8') as list_file:
        programms_list = json.loads(list_file.read())
        for programm in programms_list.keys():
            for ru_programm_name in programms_list[programm]["ru_name"]:
                if ru_programm_name in user_input:
                    os.system(programms_list[programm]["cmd"])
                    return "Открыла!"

    return "Ой, кажется я еще не научилась это открывать."


if __name__ == "__main__":
    print(weather("какая сейчас погода в ростове на дону"))
