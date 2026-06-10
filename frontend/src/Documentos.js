import React, { useState, useEffect } from "react";
import API from "./api";
import "./DocumentosTabs.css"; // Importa el CSS

function DocumentosTabs() {
  const [activeTab, setActiveTab] = useState(1);
  const [documentos, setDocumentos] = useState([]);
  const [certFile, setCertFile] = useState(null);
  const [password, setPassword] = useState("");
  const [resultado, setResultado] = useState("");

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

  const handleFirmar = async (id) => {
    if (!certFile || !password) {
      return alert("Selecciona un certificado .p12 y escribe la contraseña");
    }
    const formData = new FormData();
    formData.append("certificado", certFile);
    formData.append("password", password);

    try {
      await API.post(`/documentos/${id}/firmar`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("Documento firmado correctamente");
      window.location.reload();
    } catch (err) {
      console.error("Error al firmar documento:", err);
      alert("Error al firmar documento");
    }
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
            <p className="hint">También lo puedes arrastrar aquí</p>
            <input type="file" accept=".p12" onChange={(e) => setCertFile(e.target.files[0])} />
          </div>
          <label>Contraseña del certificado</label>
          <input type="password" placeholder="Contraseña" value={password} onChange={(e) => setPassword(e.target.value)} />

          <h4>Seleccionar Documento</h4>
          <table>
            <thead>
              <tr>
                <th>Documento</th>
                <th>Hash</th>
                <th>Acción</th>
              </tr>
            </thead>
            <tbody>
              {documentos.map((doc) => (
                <tr key={doc.id}>
                  <td>{doc.nombre}</td>
                  <td>{doc.hash}</td>
                  <td><button onClick={() => handleFirmar(doc.id)}>Firmar</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default DocumentosTabs;
