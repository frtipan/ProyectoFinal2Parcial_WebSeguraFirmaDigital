import os
from flask import Blueprint, request, jsonify
from models import Usuario
from crypto.hash_utils import verify_password
import jwt
from datetime import datetime, timedelta
from config import db
from dotenv import load_dotenv

# ✅ Cargar variables de entorno desde .env
load_dotenv()

auth_bp = Blueprint("auth", __name__)

# ✅ Usar SECRET_KEY desde entorno, no hardcodeado
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(email=data["email"]).first()
    if usuario and verify_password(data["password"], usuario.password_hash):
        token = jwt.encode(
            {"user_id": usuario.id, "exp": datetime.utcnow() + timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"mensaje": "Login correcto", "token": token})
    return jsonify({"mensaje": "Credenciales inválidas"}), 401
