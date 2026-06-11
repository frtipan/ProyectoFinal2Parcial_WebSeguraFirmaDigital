from flask import Blueprint, request, jsonify, send_file
from extensions import db
from models import Certificado
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
import io

certificados_bp = Blueprint("certificados", __name__)

# 📌 Emitir certificado auto-firmado y devolver archivo .p12
@certificados_bp.route("/", methods=["POST"])
def emitir_certificado():
    data = request.json
    if not data or "usuario_id" not in data or "password" not in data:
        return jsonify({"error": "Debe enviar usuario_id y password"}), 400

    # Generar clave privada
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Definir sujeto y emisor
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, data.get("country", "EC")),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, data.get("state", "Pichincha")),
        x509.NameAttribute(NameOID.LOCALITY_NAME, data.get("locality", "Quito")),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, data.get("organization", "MiOrganizacion")),
        x509.NameAttribute(NameOID.COMMON_NAME, data.get("common_name", "Usuario")),
    ])

    # Crear certificado válido por 1 año
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .sign(private_key, hashes.SHA256())
    )

    # Exportar a formato PKCS12 (.p12) con contraseña
    p12_data = pkcs12.serialize_key_and_certificates(
        name=b"certificado",
        key=private_key,
        cert=cert,
        cas=None,
        encryption_algorithm=serialization.BestAvailableEncryption(data["password"].encode())
    )

    # Guardar metadata en BD
    nuevo_cert = Certificado(
        usuario_id=data["usuario_id"],
        certificado=cert.public_bytes(serialization.Encoding.PEM).decode(),
        valido=True
    )
    db.session.add(nuevo_cert)
    db.session.commit()

    # Devolver archivo descargable
    return send_file(
        io.BytesIO(p12_data),
        mimetype="application/x-pkcs12",
        as_attachment=True,
        download_name=f"cert_usuario_{data['usuario_id']}.p12"
    )

# 📌 Listar certificados
@certificados_bp.route("/", methods=["GET"])
def listar_certificados():
    certs = Certificado.query.all()
    resultado = []
    for c in certs:
        expira = None
        try:
            cert_obj = x509.load_pem_x509_certificate(c.certificado.encode())
            expira = cert_obj.not_valid_after.isoformat()
        except Exception:
            pass
        resultado.append({
            "id": c.id,
            "usuario_id": c.usuario_id,
            "valido": c.valido,
            "expira": expira
        })
    return jsonify(resultado)

# 📌 Revocar certificado
@certificados_bp.route("/<int:id>/revocar", methods=["PUT"])
def revocar_certificado(id):
    cert = Certificado.query.get_or_404(id)
    cert.valido = False
    db.session.commit()
    return jsonify({"mensaje": "Certificado revocado", "id": cert.id})

# 📌 Eliminar certificado
@certificados_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_certificado(id):
    cert = Certificado.query.get_or_404(id)
    db.session.delete(cert)
    db.session.commit()
    return jsonify({"mensaje": "Certificado eliminado", "id": id})
