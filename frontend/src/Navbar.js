import React from "react";
import { useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token"); // 🔒 elimina sesión
    navigate("/login", { replace: true }); // 👉 replace evita retroceder
  };

  return (
    <nav className="navbar">
      <h3 className="navbar-title">Firma Digital</h3>
      <button onClick={handleLogout} className="logout-btn">
        Cerrar sesión
      </button>
    </nav>
  );
}

export default Navbar;
