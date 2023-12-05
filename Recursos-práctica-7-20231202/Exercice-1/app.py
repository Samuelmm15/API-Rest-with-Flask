import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, current_app

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='127.0.0.1',
        	database="flask_db",
        # user=os.environ['DB_USERNAME'],
		user="postgres",
		# password=os.environ['DB_PASSWORD']
        password="tibYDKQ8")
    return conn


@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books;')
        books = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', books=books)
    except Exception as e:
        current_app.logger.error(f"Error en la consulta a la base de datos: {e}")
        return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        try:
            title = request.form['title']
            author = request.form['author']
            pages_num = int(request.form['pages_num'])
            review = request.form['review']

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO books (title, author, pages_num, review)'
                        'VALUES (%s, %s, %s, %s)',
                        (title, author, pages_num, review))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            # Manejar la excepción de manera adecuada
            current_app.logger.error(f"Error al insertar datos en la base de datos: {e}")
            return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

    return render_template('create.html')

@app.route('/about/')
def about():
    return render_template('about.html')

# Implementación de la operación de borrado de un elemento de la base de datos, teniendo en cuenta el id del elemento a borrar
@app.route('/delete/', methods=('GET', 'POST'))
def delete():
    if request.method == 'POST':
        try:
            id = request.form['id']
            
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM books WHERE id = %s', (id,))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            current_app.logger.error(f"Error al eliminar datos de la base de datos: {e}")
            return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500

    return render_template('delete.html')

@app.route('/update/', methods=('GET', 'POST'))
def update():
    if request.method == 'POST':
        try:
            id = request.form['id']
            title = request.form['title']
            author = request.form['author']
            pages_num = int(request.form['pages_num'])
            review = request.form['review']

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('UPDATE books SET title = %s, author = %s, pages_num = %s, review = %s WHERE id = %s',
                        (title, author, pages_num, review, id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            current_app.logger.error(f"Error al actualizar datos en la base de datos: {e}")
            return render_template('error.html', error_type=type(e).__name__, error_message=str(e)), 500
            
    return render_template('update.html')
