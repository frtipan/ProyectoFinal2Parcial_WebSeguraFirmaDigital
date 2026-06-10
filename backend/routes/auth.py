import os
from flask import Blueprint, request, jsonify
from models import Usuario
from extensions import db, bcrypt   # ✅ importar extensiones desde extensions.py
from flask_jwt_extended import create_access_token
from datetime import timedelta
from dotenv import load_dotenv

# ✅ Cargar variables de entorno desde .env
load_dotenv()

auth_bp = Blueprint("auth", __name__)

# ✅ Usar SECRET_KEY desde entorno, no hardcodeado
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return jsonify({"mensaje": "Faltan credenciales"}), 400

    usuario = Usuario.query.filter_by(email=data["email"]).first()

    if usuario and bcrypt.check_password_hash(usuario.password_hash, data["password"]):
        # 🔒 Crear token JWT válido por 1 hora
        token = create_access_token(
            identity=usuario.id,
            expires_delta=timedelta(hours=1)
        )
        return jsonify({"mensaje": "Login correcto", "token": token}), 200

    # ❌ Si no coincide usuario o contraseña
    return jsonify({"mensaje": "Credenciales inválidas"}), 401
