# Proyecto Final - Plataforma Web Segura de Firma Digital

## 📌 Descripción

Este proyecto implementa un sistema web seguro de firma digital con:
- Autenticación segura con contraseñas hasheadas (SHA-256) y JWT.
- CRUD completo de usuarios, documentos y certificados.
- Criptografía AES y RSA.
- Firma digital y verificación.
- Certificados digitales simulados.
- Auditoría de acciones en base de datos.
- Pipeline DevSecOps con pruebas y escaneo de seguridad.

---

## ⚙️ Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/tuusuario/ProyectoFinal_WebSeguraFirmaDigital.git
cd ProyectoFinal_WebSeguraFirmaDigital/backend
2. Crear entorno virtual
bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
3. Instalar dependencias
bash
pip install -r requirements.txt
4. Configurar base de datos PostgreSQL
sql
CREATE DATABASE firma_digital;

Tablas dentro del schemas.sql copiar y crear las tablas en pgAdmin

Editar config.py con tu usuario y contraseña de PostgreSQL.

🚀 Ejecución
1. Arrancar backend
bash
python app.py
2. Endpoints disponibles
POST /usuarios/ → Crear usuario

GET /usuarios/ → Listar usuarios

PUT /usuarios/<id> → Actualizar usuario

DELETE /usuarios/<id> → Eliminar usuario

POST /auth/login → Login con JWT

POST /documentos/ → Subir documento (cifrado AES)

PUT /documentos/<id>/firmar → Firmar documento (RSA)

GET /documentos/<id>/verificar → Verificar firma

DELETE /documentos/<id> → Eliminar documento

POST /certificados/ → Emitir certificado

GET /certificados/ → Listar certificados

PUT /certificados/<id>/revocar → Revocar certificado

GET /logs/ → Auditoría de acciones