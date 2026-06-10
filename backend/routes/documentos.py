from flask import Blueprint, request, jsonify, Response
from extensions import db   # ✅ usar la instancia centralizada
from models import Documento, Certificado
import hashlib, base64, io
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.exceptions import InvalidSignature
from cryptography.x509 import load_pem_x509_certificate

# Librerías para incrustar firma en PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter

documentos_bp = Blueprint("documentos", __name__)

# 📌 Función para incrustar firma en PDF enriquecida
def incrustar_firma(pdf_bytes, firma_texto, certificado, estado_validacion):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 12)

    subject = certificado.subject.rfc4514_string()
    issuer = certificado.issuer.rfc4514_string()
    fecha_firma = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    can.drawString(100, 100, f"Firmado digitalmente: {firma_texto[:30]}...")
    can.drawString(100, 120, f"Estado: {estado_validacion}")
    can.drawString(100, 140, f"Firmante: {subject}")
    can.drawString(100, 160, f"Emisor: {issuer}")
    can.drawString(100, 180, f"Fecha de firma: {fecha_firma}")
    can.save()
    packet.seek(0)

    original = PdfReader(io.BytesIO(pdf_bytes))
    firma_pdf = PdfReader(packet)
    writer = PdfWriter()

    page = original.pages[0]
    page.merge_page(firma_pdf.pages[0])
    writer.add_page(page)

    for i in range(1, len(original.pages)):
        writer.add_page(original.pages[i])

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()

# 📌 Listar y subir documentos
@documentos_bp.route("/", methods=["GET", "POST"])
def documentos_handler():
    if request.method == "GET":
        documentos = Documento.query.all()
        resultado = [{
            "id": doc.id,
            "usuario_id": doc.usuario_id,
            "nombre": doc.nombre,
            "hash": doc.hash,
            "firma": doc.firma
        } for doc in documentos]
        return jsonify(resultado)

    if "file" not in request.files or request.files["file"].filename == "":
        return jsonify({"error": "No se envió archivo válido"}), 400
    
    file = request.files["file"]
    contenido = file.read()
    nombre = file.filename

    if not contenido:
        return jsonify({"error": "El archivo está vacío"}), 400

    hash_doc = hashlib.sha256(contenido).hexdigest()
    usuario_id = request.form.get("usuario_id", 1)  # ✅ tomar del form, default 1

    nuevo_doc = Documento(
        usuario_id=usuario_id,
        nombre=nombre,
        contenido=contenido,
        hash=hash_doc,
        firma=None
    )
    db.session.add(nuevo_doc)
    db.session.commit()

    return jsonify({"mensaje": "Documento subido correctamente", "hash": hash_doc}), 201

# 📌 Firmar documento
@documentos_bp.route("/<int:id>/firmar", methods=["POST"])
def firmar_documento(id):
    doc = Documento.query.get_or_404(id)

    if "certificado" not in request.files or "password" not in request.form:
        return jsonify({"error": "Debe enviar el certificado .p12 y la contraseña"}), 400

    cert_file = request.files["certificado"]
    password = request.form["password"]

    try:
        p12_data = cert_file.read()
        private_key, certificate, _ = pkcs12.load_key_and_certificates(
            p12_data,
            password.encode("utf-8")
        )
        if private_key is None or certificate is None:
            return jsonify({"error": "El certificado no contiene clave privada o certificado válido"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al cargar certificado: {str(e)}"}), 400

    try:
        hash_doc = hashlib.sha256(doc.contenido).digest()

        if isinstance(private_key, rsa.RSAPrivateKey):
            firma = private_key.sign(hash_doc, padding.PKCS1v15(), hashes.SHA256())
        elif isinstance(private_key, ec.EllipticCurvePrivateKey):
            firma = private_key.sign(hash_doc, ec.ECDSA(hashes.SHA256()))
        else:
            return jsonify({"error": "Tipo de clave no soportado"}), 400

        doc.firma = base64.b64encode(firma).decode()

        cert_pem = certificate.public_bytes(serialization.Encoding.PEM).decode()
        cert_existente = Certificado.query.filter_by(usuario_id=doc.usuario_id).first()
        if cert_existente:
            cert_existente.certificado = cert_pem
            cert_existente.valido = True
        else:
            nuevo_cert = Certificado(usuario_id=doc.usuario_id, certificado=cert_pem, valido=True)
            db.session.add(nuevo_cert)

        db.session.commit()

        return jsonify({
            "mensaje": "✅ Documento firmado correctamente",
            "documento_id": doc.id,
            "firma": doc.firma
        })
    except Exception as e:
        return jsonify({"error": f"Error al firmar documento: {str(e)}"}), 500

# 📌 Validar firma
@documentos_bp.route("/<int:id>/validar", methods=["GET"])
def validar_documento(id):
    doc = Documento.query.get_or_404(id)

    if not doc.firma:
        return jsonify({"error": "El documento no tiene firma"}), 400

    hash_doc = hashlib.sha256(doc.contenido).digest()
    cert = Certificado.query.filter_by(usuario_id=doc.usuario_id).first()
    if not cert:
        return jsonify({"error": "No existe certificado asociado al usuario"}), 400

    try:
        cert_obj = load_pem_x509_certificate(cert.certificado.encode())
        public_key = cert_obj.public_key()

        if isinstance(public_key, rsa.RSAPublicKey):
            public_key.verify(base64.b64decode(doc.firma), hash_doc, padding.PKCS1v15(), hashes.SHA256())
        elif isinstance(public_key, ec.EllipticCurvePublicKey):
            public_key.verify(base64.b64decode(doc.firma), hash_doc, ec.ECDSA(hashes.SHA256()))
        else:
            return jsonify({"error": "Tipo de clave pública no soportado"}), 400

        return jsonify({"valido": True, "mensaje": "✅ La firma es válida"})
    except InvalidSignature:
        return jsonify({"valido": False, "mensaje": "❌ La firma NO es válida"})
    except Exception as e:
        return jsonify({"error": f"Error en validación: {str(e)}"}), 500

# 📌 Abrir documento
@documentos_bp.route("/<int:id>/abrir", methods=["GET"])
def abrir_documento(id):
    doc = Documento.query.get_or_404(id)
    return Response(
        io.BytesIO(doc.contenido),
        mimetype="application/pdf",
        headers={"Content-Disposition": f"inline; filename={doc.nombre}"}
    )

# 📌 Descargar documento firmado con sello enriquecido
@documentos_bp.route("/<int:id>/descargar", methods=["GET"])
def descargar_documento(id):
    doc = Documento.query.get_or_404(id)

    if not doc.firma:
        return jsonify({"error": "El documento no tiene firma"}), 400

    cert = Certificado.query.filter_by(usuario_id=doc.usuario_id).first()
    if not cert:
        return jsonify({"error": "No existe certificado asociado al usuario"}), 400

    certificado_obj = load_pem_x509_certificate(cert.certificado.encode())

    hash_doc = hashlib.sha256(doc.contenido).digest()
    estado = "Firma válida"
    try:
        public_key = certificado_obj.public_key()
        if isinstance(public_key, rsa.RSAPublicKey):
            public_key.verify(base64.b64decode(doc.firma), hash_doc, padding.PKCS1v15(), hashes.SHA256())
        elif isinstance(public_key, ec.EllipticCurvePublicKey):
            public_key.verify(base64.b64decode(doc.firma), hash_doc, ec.ECDSA(hashes.SHA256()))
        else:
            estado = "Tipo de clave no soportado"
    except InvalidSignature:
        estado = "Firma inválida"
    except Exception as e:
        estado = f"Error validando: {str(e)}"

    pdf_firmado = incrustar_firma(doc.contenido, doc.firma, certificado_obj, estado)

    return Response(
        io.BytesIO(pdf_firmado),
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={doc.nombre.replace('.pdf','')}_firmado.pdf"}
    )

# 📌 Quitar documento
@documentos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_documento(id):
    doc = Documento.query.get_or_404(id)
    db.session.delete(doc)
    db.session.commit()
    return jsonify({"mensaje": "Documento eliminado", "id": id})
