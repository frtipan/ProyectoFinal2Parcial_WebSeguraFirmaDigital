# Proyecto Final - Plataforma Web Segura de Firma Digital

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

🔐 Configuración de variables de entorno

El proyecto usa un archivo .env para manejar credenciales y claves de forma segura.

Ejemplo de .env (NO subir a GitHub):

Código
SECRET_KEY=mi-clave-super-segura-2026-!@#$
DB_USER=postgres
DB_PASS=tu-password-segura
DB_HOST=localhost
DB_NAME=firma_digital
👉 Genera un SECRET_KEY seguro con:

bash
python -c "import secrets; print(secrets.token_hex(32))"

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