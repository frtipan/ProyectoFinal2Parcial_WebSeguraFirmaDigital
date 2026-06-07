from config import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(256))

class Documento(db.Model):
    __tablename__ = "documentos"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    nombre = db.Column(db.String(100))
    contenido = db.Column(db.LargeBinary)
    firma = db.Column(db.LargeBinary)

class Certificado(db.Model):
    __tablename__ = "certificados"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    certificado = db.Column(db.Text)
    valido = db.Column(db.Boolean, default=True)

class Log(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    accion = db.Column(db.String(100))
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    detalle = db.Column(db.Text)
