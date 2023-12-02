from flask import Flask
from flask import jsonify

app = Flask(__name__)
	
from flask import jsonify
@app.route('/numbers/')

def print_list():
    return jsonify(list(range(5)))	

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)		