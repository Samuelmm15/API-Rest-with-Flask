import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, current_app

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='127.0.0.1',
                            database="myhome",
                            user="postgres",
                            password="tibYDKQ8")
    return conn

# Para comenzar se implementa una página principal que nos permita visualizar todos los elementos.
@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM temperatures;')
        temperature = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', rooms=temperature)
    except Exception as e:
        current_app.logger.error(f"Error at the data base consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

# Implementación del primer punto, retorno de la temperatura media de todas las habitaciones.
@app.route('/average/')
def average():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT AVG(temperature) FROM temperatures;')
        average = cur.fetchall()
        cur.close()
        conn.close()
        # Se obtiene el valor de la media para que se muestre de manera correcta en el html.
        average = average[0][0]
        return render_template('average.html', average=average)
    except Exception as e:
        current_app.logger.error(f"Error at the data base consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

# Implementación del segundo punto, retorno de la temperatura máxima en las habitaciones.
@app.route('/max/')
def max():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT MAX(temperature) FROM temperatures;')
        max = cur.fetchall()
        cur.close()
        conn.close()
        # Se obtiene el valor de la temperatura máxima para que se muestre de manera correcta en el html.
        max = max[0][0]
        return render_template('max.html', max=max)
    except Exception as e:
        current_app.logger.error(f"Error at the data base consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

# Implementación del tercer punto, dado el room_id, devolver el nombre de la habitación
@app.route('/room/', methods=['GET', 'POST'])
def room_id():
    try:
        # if request.method == 'POST':
        #     room_id = request.form['room_id']
        #     print(room_id)
        #     conn = get_db_connection()
        #     cur = conn.cursor()
        #     cur.execute(f'SELECT name FROM rooms WHERE id={room_id};')
        #     roomname = cur.fetchall()
        #     cur.close()
        #     conn.close()
        #     # Se obtiene el valor del nombre de la habitación para que se muestre de manera correcta en el html.
        #     roomname = roomname[0][0]
        #     return redirect('room_name.html', room_name=roomname)
        # else:
        if request.method == 'GET':
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id FROM rooms;')
            room_id = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('room_id.html', room_id=room_id)
    except Exception as e:
        current_app.logger.error(f"Error at the data base consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

@app.route('/room/result/', methods=['POST'])
def room_result():
    try:
        room_id = request.form['room_id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name FROM rooms WHERE id=%s;', (room_id,))
        roomname = cur.fetchone()[0]
        cur.close()
        conn.close()
        return render_template('room_name.html', room_name=roomname)
    except Exception as e:
        current_app.logger.error(f"Error at the database consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500


