from flask import Flask
app = Flask(__name__)

@app.route('/<int:number>/<int:number1>/')
def add_to_numbers(number, number1):
    return "Added the two introduced numbers " + str(number + number1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)