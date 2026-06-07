CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  password_hash VARCHAR(256)
);

CREATE TABLE documentos (
  id SERIAL PRIMARY KEY,
  usuario_id INT REFERENCES usuarios(id),
  nombre VARCHAR(100),
  contenido BYTEA,
  firma BYTEA
);

CREATE TABLE certificados (
  id SERIAL PRIMARY KEY,
  usuario_id INT REFERENCES usuarios(id),
  certificado TEXT,
  valido BOOLEAN DEFAULT TRUE
);

CREATE TABLE logs (
  id SERIAL PRIMARY KEY,
  usuario_id INT REFERENCES usuarios(id),
  accion VARCHAR(100),
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  detalle TEXT
);
