from flask import Blueprint, request, jsonify
from models import Usuario, Log
from config import db
from crypto.hash_utils import hash_password

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/", methods=["POST"])
def crear_usuario():
    data = request.json
    hashed = hash_password(data["password"])
    usuario = Usuario(nombre=data["nombre"], email=data["email"], password_hash=hashed)
    db.session.add(usuario)
    db.session.commit()
    log = Log(usuario_id=usuario.id, accion="Crear Usuario", detalle=f"Usuario {usuario.email} creado")
    db.session.add(log)
    db.session.commit()
    return jsonify({"id": usuario.id, "nombre": usuario.nombre, "email": usuario.email}), 201

@usuarios_bp.route("/", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{"id": u.id, "nombre": u.nombre, "email": u.email} for u in usuarios])

@usuarios_bp.route("/<int:id>", methods=["PUT"])
def actualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json
    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.email = data.get("email", usuario.email)
    if "password" in data:
        usuario.password_hash = hash_password(data["password"])
    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado"})

@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado"})
