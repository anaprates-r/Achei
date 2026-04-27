# configuração geral da aplicação
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

#__________INITIALISATIONS____________________
app = Flask(__name__)
CORS(
    app,
    origins=["https://achei-medicamentos.vercel.app"],
    supports_credentials=True,
    allow_headers="*",
    methods=["GET", "POST", "OPTIONS"]
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


ALLOWED_EXTENSIONS = {'xls','xlsx'}
app.config['UPLOAD_FOLDER'] ="uploads"


db = SQLAlchemy(app)
