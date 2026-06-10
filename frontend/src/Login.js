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
      const res = await API.post("/auth/login", { email, password });

      if (res.data && res.data.token) {
        localStorage.setItem("token", res.data.token);
        alert("✅ Login correcto");
        navigate("/documentos"); // 👉 redirige a documentos
      } else {
        alert("❌ Credenciales inválidas");
      }
    } catch (err) {
      console.error("Error en login:", err.response?.data || err.message);
      alert("❌ Error en login. Revisa el backend.");
    }
  };

  return (
    <div className="login-container">
      <h2>Iniciar Sesión</h2>
      <input
        type="email"
        placeholder="Email"
        value={email} // ✅ mantener controlado
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Contraseña"
        value={password} // ✅ mantener controlado
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Ingresar</button>

      {/* 👉 Enlace hacia registro */}
      <p className="register-link">
        ¿No tienes cuenta? <Link to="/register">Crea una aquí</Link>
      </p>
    </div>
  );
}

export default Login;
