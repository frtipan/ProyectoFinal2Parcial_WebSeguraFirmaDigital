import React, { useState } from "react";
import API from "./api";
import { useNavigate } from "react-router-dom";
import "./Register.css";

function Register() {
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      await API.post("/usuarios/", { nombre, email, password });
      alert("✅ Usuario registrado correctamente");
      navigate("/login"); // 👉 después de registrar, vuelve al login
    } catch (err) {
      alert("❌ Error en registro");
    }
  };

  return (
    <div className="register-container">
      <h2>Registro</h2>
      <input placeholder="Nombre" onChange={(e) => setNombre(e.target.value)} />
      <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Contraseña" onChange={(e) => setPassword(e.target.value)} />
      
      {/* Botón principal de registro */}
      <button onClick={handleRegister}>Registrar</button>

      {/* Botón secundario para volver al login */}
      <button 
        className="secondary-btn" 
        onClick={() => navigate("/login")}
        style={{ marginTop: "10px" }}
      >
        Volver al inicio de sesión
      </button>
    </div>
  );
}

export default Register;
