# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import subprocess
import os
import signal
import time
# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
# import grasp
# from flask_sslify import SSLify
#
# from OpenSSL import SSL

#sslify = SSLify(app)
# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('185.243.131.130.crt')
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['GET'])
def hello():
    return "Hello"

@app.route("/", methods=['POST'])
def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']
    week = int(time.strftime('%W',time.localtime(time.time())))
    day = int(time.localtime(time.time()).tm_wday)
    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Хочу сменить номер группы",
                "Расписание на завтра",
                "Какие сегодня пары",
                "Отстань!",
            ],
            'group':'0',
            'pending':False
        }

        res['response']['text'] = 'Привет! Я смогу подсказывать тебе расписание пар, чтобы ты никогда на них не опаздывал! \n Но для начала мне нужно узнать - в какой группе ты учишься?  Напечатай только номер группы, например - 8431К '
        res['response']['tts'] = 'Привет! Пох+оже, мы еще не знак+омы. Мен+я зов+ут Ал+иса. Я с р+адостью подскаж+у тебе распис+ание пар, но для нач+ала, пож+алуйста, подскаж+и мне в как+ой гр+уппе ты учишься.'
        sug = [
            {'title': '5512', 'hide': True}

        ]
        sessionStorage[user_id]['pending'] = True
        res['response']['buttons'] = sug
        return
    if sessionStorage[user_id]['pending'] == True:
        group = req['request']['original_utterance']
        names = os.listdir('cachedsun/blue')
        if group in names:
            sessionStorage[user_id]['group'] = group
            sessionStorage[user_id]['pending'] = False
            res['response']['text'] = 'Супер! Теперь я знаю номер твоей группы!'
            res['response']['tts'] = 'Прист+упим к делу?'
            res['response']['buttons'] = getSuggests(user_id)
            return
        else:
            res['response']['text'] = 'Такой группы нет! Видимо, ты ошибся с вводом, попробуй еще раз'
            res['response']['tts'] = 'Не смогл+а найт+и так+ую гр+уппу.'
            return

    if sessionStorage[user_id]['group'] == '0':
        res['response']['text'] = 'Чтобы я смогла тебе помогать мне нужно знать номер твоей группы.'
        res['response']['tts'] = 'И всё же, сл+едует рассказ+ать мне в какой группе ты учишься'

        res['response']['buttons'] = getSuggests(user_id)
        return

    if 'группы' in req['request']['original_utterance'].lower() and sessionStorage[user_id]['group'] != '0' or 'группа' in req['request']['original_utterance'].lower()and sessionStorage[user_id]['group'] != '0':
        res['response']['text'] = 'Хорошо, давай сменим номер группы. На какую группу будем менять? Напечатай только номер группы, например - 8431К'
        res['response']['tts'] = 'Как ск+ажешь!'
        sug = [
            {'title': '5512', 'hide': True}

        ]
        sessionStorage[user_id]['pending'] = True
        sessionStorage[user_id]['group'] = '0'
        res['response']['buttons'] = sug
        return
    # Обрабатываем ответ пользователя.
    if 'сегодня' in req['request']['original_utterance'].lower() :
        # Пользователь согласился, прощаемся.
        weekapp = ''
        dayapp = ''
        if week % 2 == 0:
            weekapp = 'blue'
        else:
            weekapp = 'red'
        if day == 0 :
            dayapp = 'mon'
        elif day == 1:
            dayapp = 'tue'
        elif day == 2:
            dayapp = 'wed'
        elif day == 3:
            dayapp = 'thu'
        elif day == 4:
            dayapp = 'fri'
        elif day == 5:
            dayapp = 'sat'
        elif day == 6:
            dayapp = 'sun'
        resstr = ''
        with open('cached'+dayapp+'/'+weekapp+'/'+sessionStorage[user_id]['group'],'r') as f:
            resstr = f.read()

        res['response']['text'] = resstr
        if len(resstr)>100:
            res['response']['tts'] = 'Прид+ется попот+еть'
        else:
            res['response']['tts'] = 'Хал+ява!'
        res['response']['buttons'] = getSuggests(user_id)
        return

    if 'завтра' in req['request']['original_utterance'].lower() :
        # Пользователь согласился, прощаемся.
        weekapp = ''
        dayapp = ''

        if day == 0 :
            dayapp = 'tue'
        elif day == 1:
            dayapp = 'wed'
        elif day == 2:
            dayapp = 'thu'
        elif day == 3:
            dayapp = 'fri'
        elif day == 4:
            dayapp = 'sat'
        elif day == 5:
            dayapp = 'sun'
        elif day == 6:
            dayapp = 'mon'
            week +=1
        if week % 2 == 0:
            weekapp = 'blue'
        else:
            weekapp = 'red'
        resstr = ''
        with open('cached'+dayapp+'/'+weekapp+'/'+sessionStorage[user_id]['group'],'r') as f:
            resstr = f.read()

        res['response']['text'] = resstr
        if len(resstr)>100:
            res['response']['tts'] = 'Прид+ется попот+еть'
        else:
            res['response']['tts'] = 'Хал+ява!'
        res['response']['buttons'] = getSuggests(user_id)
        return
    if 'отстань' in req['request']['original_utterance'].lower() or 'пока' in req['request']['original_utterance'].lower() or 'счастливо' in req['request']['original_utterance'].lower():
            # Пользователь согласился, прощаемся.
            res['response']['text'] = 'Пока!'
            res['response']['tts'] = 'Ув+идимся!'
            res['response']['end_session'] = True
            return


    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Не очень понимаю, что ты хотел этим сказать.\n Может, на пары сходишь?'
    res['response']['tts'] = 'Мимо! М+ожет всё-так+и распис+ание пар подсказ+ать?'
    res['response']['buttons'] = getSuggests(user_id)

# Функция возвращает две подсказки для ответа.
def getSuggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': False}
        for suggest in session['suggests'][:]
    ]


    return suggests
