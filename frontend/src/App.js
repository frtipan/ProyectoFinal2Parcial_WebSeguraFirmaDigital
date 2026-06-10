import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";
import DocumentosTabs from "./DocumentosTabs";
import Certificados from "./Certificados";
import Navbar from "./Navbar";

// 🔒 Componente de ruta privada
const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas públicas */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rutas protegidas con Navbar */}
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
      </Routes>
    </BrowserRouter>
  );
}

export default App;
