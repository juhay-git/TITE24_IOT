import os

from flask import Flask, redirect, render_template, request
from flask_socketio import SocketIO
import sqlite3 #tietokantakirjasto
import eventlet

app = Flask(__name__)

socketio = SocketIO(app, async_mode='eventlet')

# tietokannan teko
yhteys = sqlite3.connect("mittaukset.db3")
kursori = yhteys.cursor()
kursori.execute("CREATE TABLE IF NOT EXISTS mittaukset (id INTEGER PRIMARY KEY, paiva TEXT, mittaus INTEGER)")
yhteys.commit()
yhteys.close()

mittaukset = dict() # {'maanantai': 7}

@app.route('/', methods=['GET'])
def index():
   mittaustiedot = dict()

   yhteys = sqlite3.connect("mittaukset.db3")
   kursori = yhteys.cursor()
   kursori.execute("SELECT paiva, mittaus FROM mittaukset")

   tiedot = kursori.fetchall()
   for paiva in tiedot:
      mittaustiedot[paiva[0]] = paiva[1]

   yhteys.commit()
   yhteys.close()

   print('Request for index page received')
   return render_template('chart.html', taulukko = mittaustiedot)

@app.route('/lisaa_tieto', methods=['POST'])
def lisaa_tieto():
   data = request.get_json(force=True)
   mittaustulos_lista = data['mittaus']
   #mittaukset[mittaustulos_lista[0]] = mittaustulos_lista[1]

   yhteys = sqlite3.connect("mittaukset.db3")
   kursori = yhteys.cursor()
   kursori.execute("INSERT INTO mittaukset (paiva, mittaus) VALUES (?,?)", (mittaustulos_lista[0], mittaustulos_lista[1]))
   yhteys.commit()
   yhteys.close()

   print("mittaustulos:", mittaustulos_lista)
   socketio.emit('data_update')
   return "200"

if __name__ == '__main__':
   #app.run()
   socketio.run(app, debug=True)
