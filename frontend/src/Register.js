import React, { useState } from "react";
import API from "./api";
import { useNavigate, Link } from "react-router-dom";
import "./Register.css";

function Register() {
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    if (!nombre || !email || !password) {
      alert("Por favor completa todos los campos");
      return;
    }

    try {
      await API.post("/usuarios/", { nombre, email, password });
      alert("✅ Usuario registrado correctamente");
      navigate("/login");
    } catch (err) {
      console.error(err.response?.data || err.message);
      alert("❌ Error en registro");
    }
  };

  return (
    <div className="register-container">
      <h1 className="app-title">Firma Digital</h1>
      <div className="register-box">
        <h2>Registro</h2>
        <input
          placeholder="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleRegister}>Registrar</button>

        <Link to="/login">
          <button className="secondary-btn">Volver al inicio de sesión</button>
        </Link>
      </div>
    </div>
  );
}

export default Register;
