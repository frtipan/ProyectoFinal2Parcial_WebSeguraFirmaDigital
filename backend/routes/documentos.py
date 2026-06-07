from flask import Blueprint, request, jsonify
from models import Documento, Usuario, Log
from config import db
from crypto.rsa_utils import generate_keys, sign_document, verify_signature
from crypto.aes_utils import encrypt_file, decrypt_file
import os

documentos_bp = Blueprint("documentos", __name__)

@documentos_bp.route("/", methods=["POST"])
def subir_documento():
    data = request.json
    usuario = Usuario.query.get_or_404(data["usuario_id"])
    contenido = data["contenido"].encode()
    # cifrado AES
    key = os.urandom(32)
    contenido_cifrado = encrypt_file(contenido, key)
    documento = Documento(usuario_id=usuario.id, nombre=data["nombre"], contenido=contenido_cifrado)
    db.session.add(documento)
    db.session.commit()
    log = Log(usuario_id=usuario.id, accion="Subir Documento", detalle=f"Documento {documento.nombre} subido")
    db.session.add(log)
    db.session.commit()
    return jsonify({"id": documento.id, "nombre": documento.nombre}), 201

@documentos_bp.route("/", methods=["GET"])
def listar_documentos():
    documentos = Documento.query.all()
    return jsonify([{"id": d.id, "nombre": d.nombre, "usuario_id": d.usuario_id} for d in documentos])

@documentos_bp.route("/<int:id>/firmar", methods=["PUT"])
def firmar_documento(id):
    documento = Documento.query.get_or_404(id)
    priv, pub = generate_keys()
    firma = sign_document(priv, documento.contenido)
    documento.firma = firma
    db.session.commit()
    return jsonify({"mensaje": "Documento firmado", "firma": firma.hex()})

@documentos_bp.route("/<int:id>/verificar", methods=["GET"])
def verificar_documento(id):
    documento = Documento.query.get_or_404(id)
    priv, pub = generate_keys()
    valido = verify_signature(pub, documento.contenido, documento.firma)
    return jsonify({"valido": valido})

@documentos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_documento(id):
    documento = Documento.query.get_or_404(id)
    db.session.delete(documento)
    db.session.commit()
    return jsonify({"mensaje": "Documento eliminado"})
