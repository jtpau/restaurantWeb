
import sqlite3
import json
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import urllib.parse
import urllib.request


app = Flask(__name__, template_folder='C:\\Users\\jtpau\\Desktop\\RestaurantList\\htmlRestaurantList\\templates')
CORS(app)

# Cargar el archivo SQL en la base de datos SQLite
def load_sqlite():
    conn = sqlite3.connect('restaurantes.db')
    with open('restaurants_data.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='restaurantes';")
    table_exists = cursor.fetchone()
    if table_exists:
        print("TABLE EXISTS")
    else:
        conn.executescript(sql_script)
    return conn
    
@app.route('/restaurantes')
def index():
    return render_template('probarBaseDatos.html')

@app.route('/restaurantes/resp', methods=['GET'])
def get_restaurantes():
    conn = load_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurantes")
    restaurantes = cursor.fetchall()

    sendData = []
    for row in restaurantes:
        restaurantData = {}
        restaurantData['id_restaurante']      = row[0]
        restaurantData['tipo_restaurante']    = row[1]
        restaurantData['subtipo_restaurante'] = row[2]
        restaurantData['nombre_restaurante']  = row[3]
        restaurantData['url_restaurante']     = row[4]
        sendData.append(restaurantData)
    restaurantes_json = json.dumps(sendData)

    cursor.execute("DROP TABLE IF EXISTS restaurantes")
    conn.close()
    return restaurantes_json

@app.route('/restaurantes/resp/burger', methods=['GET'])
def get_burger_restaurants():
    conn = load_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurantes WHERE tipo_restaurante='Hamburgueseria'")
    burgers = cursor.fetchall()

    sendData = []
    for row in burgers:
        burgerData = {}
        burgerData['id_restaurante']      = row[0]
        burgerData['tipo_restaurante']    = row[1]
        burgerData['subtipo_restaurante'] = row[2]
        burgerData['nombre_restaurante']  = row[3]
        burgerData['url_restaurante']     = row[4]
        sendData.append(burgerData)
    burger_json = json.dumps(sendData)

    cursor.execute("DROP TABLE IF EXISTS restaurantes")
    conn.close()
    return burger_json

@app.route('/restaurantes/resp/italian', methods=['GET'])
def get_italian_restaurants():
    conn = load_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurantes WHERE tipo_restaurante='Italiano'")
    italians = cursor.fetchall()

    sendData = []
    for row in italians:
        italianData = {}
        italianData['id_restaurante']      = row[0]
        italianData['tipo_restaurante']    = row[1]
        italianData['subtipo_restaurante'] = row[2]
        italianData['nombre_restaurante']  = row[3]
        italianData['url_restaurante']     = row[4]
        sendData.append(italianData)
    italian_json = json.dumps(sendData)

    cursor.execute("DROP TABLE IF EXISTS restaurantes")
    conn.close()
    return italian_json


@app.route('/restaurantes/add', methods=['POST'])
def add_restaurante():
    dataRestaurant = request.get_json()

    result = {}
    result['message'] = 'URL not valid' 
    
    conn = load_sqlite()
    cursor = conn.cursor()


    if restaurantExist(cursor, dataRestaurant['nombre_restaurante']):
        result['message'] = 'Restaurant already exist'
    else: 
        if is_valid_url:
            #TODO si el valor se subtipo es null poner NULL
            with open('restaurants_data.sql', 'a+') as sqlFile:
                sqlFile.write(f"INSERT INTO restaurantes (tipo_restaurante, subtipo_restaurante, nombre_restaurante, url_restaurante) VALUES ('{dataRestaurant['tipo_restaurante']}','{dataRestaurant['subtipo_restaurante']}','{dataRestaurant['nombre_restaurante']}','{dataRestaurant['url_restaurante']}');\n")
            result['message'] = 'Restaurante agregado exitosamente' 

    cursor.execute("DROP TABLE IF EXISTS restaurantes")
    conn.close()
    jsonToSend = json.dumps(result)
    print(jsonToSend)
    return jsonToSend

def is_valid_url(url):
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme and parsed.netloc:
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                return True
    except:
        pass
    return False

def restaurantExist(cursor, restaurantName):
    cursor.execute('SELECT * FROM restaurantes WHERE nombre_restaurante = ?', (restaurantName,))
    exist = cursor.fetchall()
    if exist:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True)


