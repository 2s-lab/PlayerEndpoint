from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from pygame import mixer
from urllib.request import urlopen
import hashlib

app = Flask(__name__)
api = Api(app)


class Player(Resource):
    def post(self):
        trackUrl = request.get_json()["trackUrl"]
        mp3file = urlopen(trackUrl)
        hash_object = hashlib.sha1(trackUrl.encode())
        with open('./music/' + hash_object.hexdigest() + '.mp3', 'wb') as output:
            output.write(mp3file.read())
        mixer.init()
        mixer.music.load('./music/' + hash_object.hexdigest() + '.mp3')
        mixer.music.play()
        return jsonify("playing")

    def delete(self):
        mixer.music.stop()
        return jsonify("stopped")


api.add_resource(Player, '/play')

if __name__ == '__main__':
    app.run(port=5002)
