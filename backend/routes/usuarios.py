import os
from flask import Blueprint, request, jsonify
from extensions import db, bcrypt   # ✅ importar extensiones desde extensions.py
from models import Usuario
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError   # ✅ manejar errores

load_dotenv()

usuarios_bp = Blueprint("usuarios", __name__)

# 📌 Crear usuario
@usuarios_bp.route("/", methods=["POST"])
def crear_usuario():
    data = request.json
    if not data or "nombre" not in data or "email" not in data or "password" not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    nuevo_usuario = Usuario(
        nombre=data["nombre"],
        email=data["email"],
        password_hash=hashed_pw
    )
    db.session.add(nuevo_usuario)
    try:
        db.session.commit()
        return jsonify({"mensaje": "Usuario creado correctamente"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El email ya está registrado"}), 400

# 📌 Listar usuarios
@usuarios_bp.route("/", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    resultado = [{"id": u.id, "nombre": u.nombre, "email": u.email} for u in usuarios]
    return jsonify(resultado), 200

# 📌 Actualizar usuario
@usuarios_bp.route("/<int:id>", methods=["PUT"])
def actualizar_usuario(id):
    data = request.json
    usuario = Usuario.query.get_or_404(id)

    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.email = data.get("email", usuario.email)

    if "password" in data:
        usuario.password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    try:
        db.session.commit()
        return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El email ya está registrado"}), 400

# 📌 Eliminar usuario
@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200
