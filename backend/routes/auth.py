from flask import Blueprint, request, jsonify
from models import Usuario
from crypto.hash_utils import verify_password
import jwt
from datetime import datetime, timedelta
from config import db

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "clave-secreta-super-segura"

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
