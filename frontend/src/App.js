import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Login from "./Login";
import Register from "./Register";
import DocumentosTabs from "./DocumentosTabs";
import Certificados from "./Certificados";
import Navbar from "./Navbar";
import AdminPanel from "./AdminPanel";

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" replace />;
};

function App() {
  const [rol, setRol] = useState("usuario");

  useEffect(() => {
    const storedRol = (localStorage.getItem("rol") || "usuario").toLowerCase().trim();
    setRol(storedRol);
  }, [localStorage.getItem("rol")]); // 👈 se recalcula cuando cambia el rol

  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas públicas */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rutas protegidas */}
        <Route
          path="/documentos"
          element={
            <PrivateRoute>
              <>
                <Navbar />
                <DocumentosTabs />
              </>
            </PrivateRoute>
          }
        />
        <Route
          path="/certificados"
          element={
            <PrivateRoute>
              <>
                <Navbar />
                <Certificados />
              </>
            </PrivateRoute>
          }
        />

        {/* Ruta exclusiva admin */}
        <Route
          path="/admin"
          element={
            <PrivateRoute>
              {rol === "admin" ? (
                <>
                  <Navbar />
                  <AdminPanel />
                </>
              ) : (
                <Navigate to="/documentos" replace />
              )}
            </PrivateRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
