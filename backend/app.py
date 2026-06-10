import os
from flask import Flask
from dotenv import load_dotenv
from extensions import db, bcrypt, jwt   # ✅ importar extensiones centralizadas
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
from flask_cors import CORS

# Blueprints
from routes.usuarios import usuarios_bp
from routes.documentos import documentos_bp
from routes.certificados import certificados_bp
from routes.auth import auth_bp

# ✅ Cargar variables de entorno
load_dotenv()

# ✅ Inicializar aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default-secret")

# 🔑 Configuración JWT (necesaria para flask_jwt_extended)
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

# ✅ Inicializar extensiones
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)

# ✅ Configurar CORS
CORS(
    app,
    resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# 📌 Registrar Blueprints
app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
app.register_blueprint(documentos_bp, url_prefix="/api/documentos")
app.register_blueprint(certificados_bp, url_prefix="/api/certificados")
app.register_blueprint(auth_bp, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
