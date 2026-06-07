from flask import Flask
from config import db, SQLALCHEMY_DATABASE_URI
from routes.usuarios import usuarios_bp
from routes.documentos import documentos_bp
from routes.certificados import certificados_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = 'clave-secreta-super-segura'

db.init_app(app)

# Registrar Blueprints
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(documentos_bp, url_prefix="/documentos")
app.register_blueprint(certificados_bp, url_prefix="/certificados")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
