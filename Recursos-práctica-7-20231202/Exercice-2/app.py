import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, current_app
import json

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='127.0.0.1',
                            database="myhome",
                            user="postgres",
                            password="tibYDKQ8")
    return conn

# Point 0
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

# Point 1
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

# Point 2
@app.route('/max/')
def max():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT MAX(temperature) FROM temperatures;')
        max = cur.fetchall()
        cur.close()
        conn.close()
        max = max[0][0]
        return render_template('max.html', max=max)
    except Exception as e:
        current_app.logger.error(f"Error at the data base consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

# Point 3
@app.route('/room/', methods=['GET'])
def room_id():
    try:
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

# Point 4
@app.route('/room_temperature_id/', methods=['GET'])
def room_temperature_id():
    try:
        if request.method == 'GET':
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id FROM rooms;')
            room_id = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('room_temperature_id.html', room_id=room_id)
    except Exception as e:
        current_app.logger.error(f"Error at the data base consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

@app.route('/room_temperature_id/result/', methods=['POST'])
def room_temperature_id_result():
    try:
        roomID = request.form['room_id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT AVG(temperature) FROM temperatures WHERE room_id=%s;', (roomID,))
        temperature = cur.fetchall()
        cur.close()
        conn.close()
        temperature = temperature[0][0]
        return render_template('room_temperature.html', room_id=roomID,room_temperature=temperature)
    except Exception as e:
        current_app.logger.error(f"Error at the data base consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

# Point 5
@app.route('/room_temperature_id_min/', methods=['GET'])
def room_temperature_id_min():
    try:
        if request.method == 'GET':
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id FROM rooms;')
            room_id = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('room_temperature_id_min.html', room_id=room_id)
    except Exception as e:
        current_app.logger.error(f"Error at the data base consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

@app.route('/room_temperature_id_min/result/', methods=['POST'])
def room_temperature_id_min_result():
    try:
        roomID = request.form['room_id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT MIN(temperature) FROM temperatures WHERE room_id=%s;', (roomID,))
        temperature = cur.fetchall()
        cur.execute('SELECT name FROM rooms WHERE id=%s;', (roomID,))
        roomname = cur.fetchone()[0]
        cur.close()
        conn.close()
        temperature = temperature[0][0]
        # json format
        data = {
            "id": roomID,
            "name": roomname,
            "min_temperature": temperature
        }
        return render_template('room_temperature_id_min_result.html', json_data=json.dumps(data))
    except Exception as e:
        current_app.logger.error(f"Error at the data base consultation: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500



