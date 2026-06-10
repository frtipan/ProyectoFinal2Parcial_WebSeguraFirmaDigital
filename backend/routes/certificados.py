from flask import Blueprint, request, jsonify
from config import db
from models import Certificado
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12

certificados_bp = Blueprint("certificados", __name__)

# 📌 Generar certificado X.509 auto-firmado dinámico
@certificados_bp.route("/", methods=["POST"])
def generar_certificado():
    data = request.json
    if not data or "usuario_id" not in data:
        return jsonify({"error": "Debe enviar usuario_id"}), 400

    # 🔑 Datos dinámicos con valores por defecto
    country = data.get("country", "EC")
    state = data.get("state", "Pichincha")
    locality = data.get("locality", "Quito")
    organization = data.get("organization", "MiOrganizacion")
    common_name = data.get("common_name", "Usuario")

    # Generar clave privada RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Definir sujeto y emisor (auto-firmado)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
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

    # Exportar certificado a PEM
    cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode()

    # Guardar en BD
    nuevo_cert = Certificado(
        usuario_id=data["usuario_id"],
        certificado=cert_pem,
        valido=True
    )
    db.session.add(nuevo_cert)
    db.session.commit()

    return jsonify({
        "mensaje": "Certificado generado",
        "certificado": cert_pem
    }), 201

# 📌 Listar certificados
@certificados_bp.route("/", methods=["GET"])
def listar_certificados():
    certs = Certificado.query.all()
    resultado = []
    for c in certs:
        try:
            cert_obj = x509.load_pem_x509_certificate(c.certificado.encode())
            expira = cert_obj.not_valid_after.isoformat()
        except Exception:
            expira = None
        resultado.append({
            "id": c.id,
            "usuario_id": c.usuario_id,
            "certificado": c.certificado,
            "valido": c.valido,
            "expira": expira
        })
    return jsonify(resultado)

# 📌 Validar certificado (.p12)
@certificados_bp.route("/validar", methods=["POST", "OPTIONS"])
def validar_certificado():
    if request.method == "OPTIONS":
        return jsonify({"mensaje": "Preflight OK"}), 200

    cert_file = request.files.get("certificado")
    password = request.form.get("password")

    if not cert_file or not password:
        return jsonify({"error": "Falta certificado o contraseña"}), 400

    try:
        p12_data = cert_file.read()
        private_key, certificate, _ = pkcs12.load_key_and_certificates(
            p12_data, password.encode()
        )

        # ✅ Verificar expiración
        if certificate.not_valid_after < datetime.utcnow():
            return jsonify({
                "detalle": "❌ Certificado expirado",
                "expira": certificate.not_valid_after.isoformat()
            }), 400

        return jsonify({
            "detalle": "✅ Certificado válido",
            "expira": certificate.not_valid_after.isoformat()
        }), 200

    except Exception as e:
        return jsonify({"error": f"❌ Certificado inválido: {str(e)}"}), 400
