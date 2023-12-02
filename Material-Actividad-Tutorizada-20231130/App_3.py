from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/person/')
def hello():
    return jsonify({'name':'Jimit',
                    'address':'India'})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)					