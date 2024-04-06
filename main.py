from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

storageSession = {}


def get_suggests(user_id):
    session = storageSession[user_id]
    suggests = [{'title': suggest, 'hide': True} for suggest in session['suggests'][:2]]
    session['suggests'] = session['suggests'][1:]
    storageSession[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "LADNA",
            "url": "https://eda.yandex.ru/kaluga",
            "hide": True
        })
    return suggests


def handle_dialog(request, response):
    user_id = request['session']['user_id']
    if request['session']['new']:
        storageSession[user_id] = {
            'suggests': [
                "ne hochu",
                "ne budu",
                "otstan",
                "ne bejte"
            ]
        }
        response['response']['text'] = "Privet, kupi mish!!!"
        response['response']['buttons'] = get_suggests(user_id)
        return
    if request['request']['original_utterance'].lower() in [
        "ladno",
        "kupliu",
        "pokupaju",
        "horosho",
        "uzhe kupil",
        "ladna"
    ]:
        response['response']['text'] = 'A jeshe mish mozhno zakazat na Yandex.Jeda i v samokat!'
        response['response']['end_session'] = True
        return
    response['response']['text'] = \
        f"Vse govoriat {request['request']['original_utterance']}, a ti kupi mish!!!"
    response['response']['button'] = get_suggests(user_id)


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
    app.run()
