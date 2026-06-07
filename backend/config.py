from flask_sqlalchemy import SQLAlchemy

DB_USER = "postgres"
DB_PASS = "12345"
DB_HOST = "localhost"
DB_NAME = "firma_digital"

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()
