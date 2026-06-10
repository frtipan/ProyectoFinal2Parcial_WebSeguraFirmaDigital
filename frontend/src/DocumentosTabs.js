import React, { useState, useEffect } from "react";
import API from "./api";
import "./DocumentosTabs.css";

function DocumentosTabs() {
  const [activeTab, setActiveTab] = useState(1);
  const [documentos, setDocumentos] = useState([]);
  const [certFile, setCertFile] = useState(null);
  const [docFile, setDocFile] = useState(null);
  const [password, setPassword] = useState("");
  const [resultado, setResultado] = useState("");
  const [firmaInvisible, setFirmaInvisible] = useState(false);

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const res = await API.get("/documentos/");
        setDocumentos(res.data);
      } catch (err) {
        console.error("Error al cargar documentos:", err);
      }
    };
    fetchDocs();
  }, []);

  // 📌 Subir documento
  const uploadDocumento = async () => {
    if (!docFile) {
      setResultado("Selecciona un documento primero");
      return;
    }
    try {
      const formData = new FormData();
      formData.append("file", docFile, docFile.name);

      console.log("Archivo que se envía:", docFile.name);

      const res = await API.post("/documentos/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResultado(res.data.mensaje || "Documento subido correctamente");

      const lista = await API.get("/documentos/");
      setDocumentos(lista.data);
    } catch (err) {
      console.error("Error subiendo documento:", err.response?.data || err);
      setResultado(`❌ Error al subir documento: ${err.response?.data?.error || "Error desconocido"}`);
    }
  };

  // 📌 Abrir documento
  const handleAbrir = (doc) => {
    window.open(`http://127.0.0.1:5000/api/documentos/${doc.id}/abrir`, "_blank");
  };

  // 📌 Descargar documento firmado
  const handleDescargarFirmado = (doc) => {
    window.open(`http://127.0.0.1:5000/api/documentos/${doc.id}/descargar`, "_blank");
  };

  // 📌 Quitar documento
  const handleQuitar = async (id) => {
    try {
      await API.delete(`/documentos/${id}`);
      setDocumentos(documentos.filter((doc) => doc.id !== id));
      setResultado("✅ Documento eliminado");
    } catch (err) {
      console.error("Error al quitar documento:", err.response?.data || err);
      setResultado(`❌ Error al eliminar documento: ${err.response?.data?.error || "Error desconocido"}`);
    }
  };

  // 📌 Firmar documento
  const handleFirmar = async (id) => {
    if (!certFile || !password) {
      return alert("Selecciona un certificado .p12 y escribe la contraseña");
    }

    const formData = new FormData();
    formData.append("certificado", certFile, certFile.name);
    formData.append("password", String(password));
    formData.append("firmaInvisible", firmaInvisible ? "true" : "false");

    try {
      await API.post(`/documentos/${id}/firmar`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResultado("✅ Documento firmado correctamente");

      const lista = await API.get("/documentos/");
      setDocumentos(lista.data);
    } catch (err) {
      console.error("Error al firmar documento:", err.response?.data || err);
      setResultado(`❌ Error al firmar documento: ${err.response?.data?.error || "Error desconocido"}`);
    }
  };

  // 📌 Validar certificado
  const handleValidarCertificado = async () => {
    if (!certFile || !password) {
      return alert("Selecciona un certificado y contraseña");
    }

    const formData = new FormData();
    formData.append("certificado", certFile, certFile.name);
    formData.append("password", String(password));

    try {
      const res = await API.post("/certificados/validar", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResultado(res.data.detalle || "✅ Certificado válido");
    } catch (err) {
      console.error("Error al validar certificado:", err.response?.data || err);
      setResultado(`❌ Error al validar certificado: ${err.response?.data?.error || "Error desconocido"}`);
    }
  };

  // 📌 Validar documento
  const handleValidar = async (id) => {
    try {
      const res = await API.get(`/documentos/${id}/validar`);
      setResultado(res.data.valido ? "✅ La firma es válida" : "❌ La firma NO es válida");
    } catch (err) {
      console.error("Error al validar documento:", err.response?.data || err);
      setResultado(`❌ Error al validar documento: ${err.response?.data?.error || "Error desconocido"}`);
    }
  };

  // 📌 Restablecer
  const handleRestablecer = () => {
    setCertFile(null);
    setDocFile(null);
    setPassword("");
    setResultado("");
    setFirmaInvisible(false);
  };

  return (
    <div className="documentos-tabs">
      {/* Menú de pestañas */}
      <div className="tabs">
        <button className={activeTab === 1 ? "active" : ""} onClick={() => setActiveTab(1)}>Firmar Documento</button>
        <button className={activeTab === 2 ? "active" : ""} onClick={() => setActiveTab(2)}>Verificar Documento</button>
        <button className={activeTab === 3 ? "active" : ""} onClick={() => setActiveTab(3)}>Validar Certificado</button>
      </div>

      {/* Panel Firmar Documento */}
      {activeTab === 1 && (
        <div className="panel">
          <h3>Firmar Documento</h3>
          <div className="drop-area">
            <p>Buscar Certificado</p>
            <input type="file" accept=".p12" onChange={(e) => setCertFile(e.target.files[0])} />
          </div>

          <label>Contraseña del certificado</label>
          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <div className="drop-area">
            <p>Buscar Documento(s)</p>
            <input type="file" accept=".pdf,.doc,.docx" onChange={(e) => setDocFile(e.target.files[0])} />
          </div>

          <button onClick={uploadDocumento}>Subir documento</button>
          <table>
            <thead>
              <tr>
                <th>Documento</th>
                <th>Abrir</th>
                <th>Descargar firmado</th>
                <th>Quitar</th>
                <th>Estado</th>
                <th>Acción</th>
              </tr>
            </thead>
            <tbody>
              {documentos.map((doc) => (
                <tr key={doc.id}>
                  <td>{doc.nombre}</td>
                  <td><button onClick={() => handleAbrir(doc)}>Abrir</button></td>
                  <td>{doc.firma ? <button onClick={() => handleDescargarFirmado(doc)}>Descargar firmado</button> : "Sin firma"}</td>
                  <td><button onClick={() => handleQuitar(doc.id)}>Quitar</button></td>
                  <td>{doc.firma ? "Firmado" : "Sin firma"}</td>
                  <td><button onClick={() => handleFirmar(doc.id)}>Firmar</button></td>
                </tr>
              ))}
            </tbody>
          </table>
          {resultado && <div className="resultado">{resultado}</div>}
        </div>
      )}

      {/* Panel Validar Documento */}
{activeTab === 2 && (
  <div className="panel">
    <h3>Validar Documento</h3>
    <table>
      <thead>
        <tr>
          <th>Documento</th>
          <th>Abrir</th>
          <th>Quitar</th>
          <th>Estado</th>
          <th>Detalle</th>
        </tr>
      </thead>
      <tbody>
        {documentos.length === 0 ? (
          <tr>
            <td colSpan="5">0 DOCUMENTO(S) SELECCIONADO(S)</td>
          </tr>
        ) : (
          documentos.map((doc) => (
            <tr key={doc.id}>
              <td>{doc.nombre}</td>
              <td><button onClick={() => handleAbrir(doc)}>Abrir</button></td>
              <td><button onClick={() => handleQuitar(doc.id)}>Quitar</button></td>
              <td>{doc.firma ? "Firmado" : "Sin firma"}</td>
              <td><button onClick={() => handleValidar(doc.id)}>Validar</button></td>
            </tr>
          ))
        )}
      </tbody>
    </table>

    {resultado && <div className="resultado">{resultado}</div>}
  </div>
)}


      {/* Panel Validar Certificado */}
      {activeTab === 3 && (
        <div className="panel">
          <h3>Validar Certificado</h3>
          <div className="drop-area">
            <p>Buscar Certificado</p>
            <input type="file" accept=".p12" onChange={(e) => setCertFile(e.target.files[0])} />
          </div>

          <label>Contraseña</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button onClick={handleValidarCertificado}>Validar</button>
          <button onClick={handleRestablecer}>Restablecer</button>

          {resultado && <div className="resultado">{resultado}</div>}
        </div>
      )}
    </div>
  );
}

export default DocumentosTabs;