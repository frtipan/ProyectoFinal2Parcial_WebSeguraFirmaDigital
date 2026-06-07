from flask import Blueprint, request, jsonify
from models import Certificado, Usuario, Log
from config import db
from crypto.rsa_utils import generate_keys
from crypto.cert_utils import generate_certificate
from cryptography.hazmat.primitives import serialization

certificados_bp = Blueprint("certificados", __name__)

@certificados_bp.route("/", methods=["POST"])
def emitir_certificado():
    data = request.json
    usuario = Usuario.query.get_or_404(data["usuario_id"])
    priv, pub = generate_keys()
    cert = generate_certificate(priv, pub, usuario.nombre)
    cert_info = Certificado(
        usuario_id=usuario.id,
        certificado=cert.public_bytes(serialization.Encoding.PEM).decode("utf-8"),
        valido=True
    )
    db.session.add(cert_info)
    db.session.commit()
    log = Log(usuario_id=usuario.id, accion="Emitir Certificado", detalle=f"Certificado emitido para {usuario.email}")
    db.session.add(log)
    db.session.commit()
    return jsonify({"id": cert_info.id, "usuario_id": usuario.id, "valido": cert_info.valido}), 201

@certificados_bp.route("/", methods=["GET"])
def listar_certificados():
    certificados = Certificado.query.all()
    return jsonify([{"id": c.id, "usuario_id": c.usuario_id, "valido": c.valido} for c in certificados])

@certificados_bp.route("/<int:id>/revocar", methods=["PUT"])
def revocar_certificado(id):
    cert = Certificado.query.get_or_404(id)
    cert.valido = False
    db.session.commit()
    return jsonify({"mensaje": "Certificado revocado"})
