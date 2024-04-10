from flask import Flask, request, jsonify
import logging
import json
import random

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

storageSession = {}

cities = {
    'СПБ': ['997614/3247562f0aef7585d4df', '997614/a47bcf710c2e60fd8fdb'],
    'Казань': ['1521359/d7e1bafe1e82119028ab'],
    'Калининград': ['1521359/87d367ac5616c3cb6ae2'],
    'Калуга': ['1540737/251c4a27485239ce69ca']
}


def get_city(request):
    for entity in request['request']['nlu']['entities']:
        if entity['type'] == "YANDEX.FIO":
            return entity['value'].get('first_name', None)


def get_first_name(request):
    for entity in request['request']['nlu']['entities']:
        if entity['type'] == "YANDEX.GEO":
            return entity['value'].get('city', None)


def handle_dialog(request, response):
    user_id = request['session']['user_id']
    if request['session']['new']:
        response['response']['text'] = 'Привет! назови своё имя!'
        storageSession[user_id] = {
            'first_name': None
        }
        return
    if storageSession[user_id]['first_name'] is None:
        first_name = get_first_name(request)
        if first_name is None:
            response['response']['text'] = 'Не расслышал, повторите пожалуйста!'
        else:
            storageSession[user_id]['first_name'] = first_name
            response['response']['text'] = (f'Приятно познакомиться, {first_name.title()}' \
                                            f'Меня зовут Алиса ' \
                                            f'Какой город показать?')
            response['response']['buttons'] = [
                {
                    'title': city.title(),
                    'hide': True
                }
                for city in cities
            ]
    else:
        city = get_city(request)
        if city in cities:
            response['response']['card'] = {}
            response['response']['card']['type'] = 'BigImage'
            response['response']['card']['title'] = 'Этот город я знаю'
            response['response']['card']['image_id'] = random.choice(cities[city])
            response['response']['text'] = 'Я угадал'
        else:
            response['response']['text'] = 'Первый раз слышу о таком городе' \
                                           'Попробуем ещё раз?'


@app.route('/post', methods=['POST'])
def main():
    logging.info(f"Request: {request.json!r}")
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    logging.info(f"Response: {response}!r")
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5000)
