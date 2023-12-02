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