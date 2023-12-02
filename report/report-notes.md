# API REST con Python y PostgreSQL

## Actividad 1

1. Instalación del framework Flask y la biblioteca de python psycopg2-binary.

Para la instalación de dicho framework se hace uso de los siguientes comandos:

```bash
$ python3 -m pip install flask

$ python3 -m pip install psycopg2-binary
```

Cabe destacar que los comandos anteriores se pueden instalar en la máquina local o en un entorno virtual de python.

2. Despliegue de la aplicación web que aparece en la carperta de recursos de la práctica 7.

Para el despliegue de la aplicación denominada como  `app.py`, la cual se encuentra desarrollada de manera previa, y, la cual hace uso de flask para implementar una api rest que permite en esta ocasión realizar operaciones CRUD sobre una base de datos de PostgreSQL, se hace uso del siguiente comando:

```bash
$ flask --app app.py run --host 0.0.0.0 --port 8080
```

Una vez se tiene el hecho de como se despliega una aplicación web con flask, se realiza la implementación de la base de datos de PostgreSQL a continuación en la siguiente interacción.

3. Implementación de la base de datos de PostgreSQL.

Para la implementación de la base de datos de PostgreSQL, en primer lugar se debe de crear la base de datos dentro del propio gestor de base de datos, para ello se hace uso del siguiente comando:

```bash
$ sudo -i -u postgres
$ psql
$ CREATE DATABASE flask_db;
```

Una vez se tiene creada la base de datos dentro de PostgreSQL, se procede a la inserción de al menos 9 registros dentro de la base de datos creada de manera anterior, es por ello que, se hace uso del script denominado como `init_db.py` el cual se encuentra dentro de la carpeta de recursos de la práctica 7. Una vez se tiene dicho script, se realiza la modificación de este de la siguiente manera para que cumpla los requisitos de la insersión de 9 registros  y el control de excepciones en el código.

Todo esto se puede observar a continuación:

```python
import os
import psycopg2

conn = psycopg2.connect(
        host="127.0.0.1",
        database="flask_db",
        #user=os.environ['DB_USERNAME'],
        #password=os.environ['DB_PASSWORD']
		user='postgres',
        password='tibYDKQ8')

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS books;')
cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                 'title varchar (150) NOT NULL,'
                                 'author varchar (50) NOT NULL,'
                                 'pages_num integer NOT NULL,'
                                 'review text,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('A Tale of Two Cities',
             'Charles Dickens',
             489,
             'A great classic!')
            )


cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('Anna Karenina',
             'Leo Tolstoy',
             864,
             'Another great classic!')
            )

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('The Great Gatsby',
             'F. Scott Fitzgerald',
             218,
             'Another great classic!')
            )

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('One Hundred Years of Solitude',
             'Gabriel García Márquez',
             417,
             'Another great classic!')
            )

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('A Passage to India',
             'E. M. Forster',
             378,
             'A great classic!')
            )

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('The Adventures of Huckleberry Finn',
             'Mark Twain',
             366,
             'A great classic!')
            )

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('The Catcher in the Rye',
             'J. D. Salinger',
             234,
             'Another great classic!')
            )

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('The Grapes of Wrath',
             'John Steinbeck',
             464,
             'A great classic!')
            )

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('The Great Gatsby',
             'F. Scott Fitzgerald',
             218,
             'Another great classic!')
            )

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('The Odyssey',
             'Homer',
             213,
             'A great classic!')
            )

# Exception handling example
try:
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    print(books)
except psycopg2.Error as e:
    print(f'ERROR: {e}')
    conn.rollback()


conn.commit()

cur.close()
conn.close()
```

Una vez se tiene el script modificado, se procede a ejecutarlo de la siguiente manera:

```bash
$ python3 init_db.py
```

Tras estos pasos, se tiene la base de datos implementada y con registros dentro de esta.

4. Personalización de la referencia About.

Para la personalización de la referencia About, en primer lugar se crea una nueva ruta dentro del archivo `app.py` de la siguiente manera:

```python
@app.route('/about/')
def about():
    return render_template('about.html')
```

Una vez se tiene la ruta creada, se procede a crear el archivo `about.html` dentro de la carpeta de templates de la siguiente manera:

```html
{% extends 'base.html' %}

{% block content %}
    <h1>{% block title %} About us {% endblock %}</h1>
    <p> This is the about page </p>
    <h2> {% block subtitle %} Project Components {% endblock %}</h2>
    <p> Samuel Martín Morales --> alu0101359526@ull.edu.es </p>
    <p> Jorge Domínguez  González --> alu0101330600@ull.edu.es </p>
{% endblock %}
```

Una vez se tiene todo esto anterior, se modifica una línea dentro del archivo `base.html` de la siguiente manera:

```html
<a href="{{ url_for('about') }}">About</a>
```

5. Verificación del funcionamiento de la operación de visualización de lo registros de la base de datos.

El funcionamiento de la operación de visualización de los registros de la base de datos es correcta, es decir, se muestran todos los registros de la base de datos de manera correcta. Por tanto, se realiza la implementación del control de excepciones en el código de la siguiente manera:

```python
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
```

Por otra parte se puede observar a continuación la implementación de una página de error en el caso de que se produzca un error en la base de datos:

```python 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error en la aplicación</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }

        .error-container {
            text-align: center;
        }

        h1 {
            color: #d64161;
        }

        p {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>Error en la aplicación</h1>
        <p>Ocurrió un error de tipo <strong>{{ error_type }}</strong>.</p>
        <p>Detalle del error: <em>{{ error_message }}</em></p>
        <p>Por favor, inténtalo de nuevo más tarde.</p>
    </div>
</body>
</html>
```

6. Verificación del funcionamiento de la operación de inserción de un nuevo registro en la base de datos.

Tras la revisión del funcionamiento de la página denominada como `create`, es decir, la página de inserción de nuevos registros dentro de la base de datos, se puede observar que el funcionamiento de esta es correcto, es decir, se insertan nuevos registros dentro de la base de datos de manera correcta. Por tanto, se realiza la implementación del control de excepciones en el código de la siguiente manera:

```python
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
```

7. Construcción de una nueva operación dentro de la API REST que se encargue de la operación de borrado de un registro de la base de datos a partir del ID.