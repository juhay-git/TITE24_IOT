import os

from flask import Flask, redirect, render_template, request
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__)

socketio = SocketIO(app, async_mode='eventlet')

mittaukset = dict() # {'maanantai': 7}

@app.route('/', methods=['GET'])
def index():
   print('Request for index page received')
   return render_template('index.html', taulukko = mittaukset)

@app.route('/lisaa_tieto', methods=['POST'])
def lisaa_tieto():
   data = request.get_json(force=True)
   mittaustulos_lista = data['mittaus']
   mittaukset[mittaustulos_lista[0]] = mittaustulos_lista[1]
   print("mittaustulos:", mittaustulos_lista)
   socketio.emit('data_update')
   return "200"

if __name__ == '__main__':
   #app.run()
   socketio.run(app, debug=True)
