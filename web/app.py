from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

app.config.from_pyfile('config.py')

CORS(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')