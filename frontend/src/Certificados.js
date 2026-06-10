import React, { useState, useEffect } from "react";
import API from "./api";
import "./Certificados.css";

function Certificados() {
  const [certs, setCerts] = useState([]);

  const fetchCerts = async () => {
    const res = await API.get("/certificados");
    setCerts(res.data);
  };

  useEffect(() => { fetchCerts(); }, []);

  return (
    <div className="certs-container">
      <h2>Certificados</h2>
      <ul>
        {certs.map((c) => (
          <li key={c.id}>
            Documento: {c.documento_id} | Firma: {c.firma} | Fecha: {c.fecha_emision}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Certificados;
