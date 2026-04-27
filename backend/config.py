# configuração geral da aplicação
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

#__________INITIALISATIONS____________________
app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {
        "origins": "https://achei-medicamentos.vercel.app"
    }},
    supports_credentials=True
)
@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "https://achei-medicamentos.vercel.app"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


ALLOWED_EXTENSIONS = {'xls','xlsx'}
app.config['UPLOAD_FOLDER'] ="uploads"


db = SQLAlchemy(app)
