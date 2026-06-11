from extensions import db   # ✅ importar desde extensions.py

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), default="usuario", nullable=False)  # ✅ rol obligatorio

    # Relación con documentos, certificados y logs
    documentos = db.relationship("Documento", backref="usuario", lazy=True, cascade="all, delete-orphan")
    certificados = db.relationship("Certificado", backref="usuario", lazy=True, cascade="all, delete-orphan")
    logs = db.relationship("Log", backref="usuario", lazy=True, cascade="all, delete-orphan")


class Documento(db.Model):
    __tablename__ = "documentos"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)   # nombre más largo
    contenido = db.Column(db.LargeBinary, nullable=False) # binario para guardar archivo
    hash = db.Column(db.String(64), nullable=False)       # SHA-256 en hex
    firma = db.Column(db.Text, nullable=True)             # firma en base64


class Certificado(db.Model):
    __tablename__ = "certificados"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    certificado = db.Column(db.Text, nullable=False)  # PEM del certificado
    valido = db.Column(db.Boolean, default=True)


class Log(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    accion = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, server_default=db.func.now())
    detalle = db.Column(db.Text)
