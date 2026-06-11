import React, { useState } from "react";
import API from "./api";
import { useNavigate, Link } from "react-router-dom";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!email || !password) {
      alert("Por favor ingresa email y contraseña");
      return;
    }

    try {
      // 👉 Llamada al backend
      const res = await API.post("/auth/login", { email, password });

      if (res.data?.token) {
        // ✅ Normalizar rol a minúsculas y sin espacios
        const rol = (res.data.rol || "usuario").toLowerCase().trim();

        // Guardar token y rol en localStorage
        localStorage.setItem("token", res.data.token);
        localStorage.setItem("rol", rol);

        console.log("ROL recibido:", rol);

        alert("✅ Credenciales válidas");

        // 👉 Redirigir según rol
        if (rol === "admin") {
          navigate("/admin"); // Panel exclusivo administrador
        } else {
          navigate("/documentos"); // Panel normal de usuario
        }
      } else {
        alert("❌ Credenciales inválidas");
      }
    } catch (err) {
      console.error("Error en login:", err.response?.data || err.message);
      alert("❌ Credenciales inválidas");
    }
  };

  return (
    <div className="login-container">
      <h1 className="app-title">Firma Digital</h1>
      <div className="login-box">
        <h2>Iniciar Sesión</h2>
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
        <button onClick={handleLogin}>Ingresar</button>

        <p className="register-link">
          ¿No tienes cuenta? <Link to="/register">Crea una aquí</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
