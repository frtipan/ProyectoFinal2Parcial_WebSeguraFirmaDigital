import os
from flask import Flask
from dotenv import load_dotenv
from config import db, SQLALCHEMY_DATABASE_URI
from routes.usuarios import usuarios_bp
from routes.documentos import documentos_bp
from routes.certificados import certificados_bp
from routes.auth import auth_bp

load_dotenv()

app = Flask(__name__)

# ✅ Usar variables de entorno en vez de hardcodear
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default-secret")

db.init_app(app)

# Registrar Blueprints
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(documentos_bp, url_prefix="/documentos")
app.register_blueprint(certificados_bp, url_prefix="/certificados")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # ❌ No usar debug=True ni host=0.0.0.0 en producción
    app.run(host="127.0.0.1", port=5000)
