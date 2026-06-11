import React from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();
  const rol = localStorage.getItem("rol"); // 👉 leer rol guardado en login

  const handleLogout = () => {
    localStorage.removeItem("token"); // 🔒 elimina sesión
    localStorage.removeItem("rol");    // ✅ limpiar rol también
    navigate("/login", { replace: true }); // 👉 replace evita retroceder
  };

  return (
    <nav className="navbar">
      <h3 className="navbar-title">Firma Digital</h3>

      <div className="navbar-links">
        {rol === "admin" ? (
          // 👉 enlaces exclusivos para administrador
          <>
            <Link to="/admin"></Link>
          </>
        ) : (
          // 👉 enlaces para usuario normal
          <>
            <Link to="/documentos">Documentos</Link>
            <Link to="/certificados">Certificados</Link>
          </>
        )}
      </div>

      <button onClick={handleLogout} className="logout-btn">
        Cerrar sesión
      </button>
    </nav>
  );
}

export default Navbar;
