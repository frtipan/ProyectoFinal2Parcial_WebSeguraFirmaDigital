import React, { useEffect, useState } from "react";
import API from "./api";

function AdminPanel() {
  const [usuarios, setUsuarios] = useState([]);
  const [certificados, setCertificados] = useState([]);

  useEffect(() => {
    cargarUsuarios();
    cargarCertificados();
  }, []);

  const cargarUsuarios = async () => {
    try {
      const res = await API.get("/usuarios/");
      setUsuarios(res.data);
    } catch (err) {
      console.error(err);
      alert("❌ Error al cargar usuarios");
    }
  };

  const cargarCertificados = async () => {
    try {
      const res = await API.get("/certificados/");
      setCertificados(res.data);
    } catch (err) {
      console.error(err);
      alert("❌ Error al cargar certificados");
    }
  };

  // 🟢 Crear usuario
  const crearUsuario = async () => {
    const nombre = prompt("Nombre del usuario:");
    const email = prompt("Email del usuario:");
    const password = prompt("Contraseña:");
    const rol = prompt("Rol (usuario/admin):", "usuario");

    if (!nombre || !email || !password) return;

    try {
      await API.post("/usuarios/", {
        nombre,
        email,
        password,
        rol: rol?.toLowerCase() // 👈 normalizar rol
      });
      alert("✅ Usuario creado");
      cargarUsuarios();
    } catch (err) {
      console.error(err.response?.data || err);
      alert("❌ Error al crear usuario");
    }
  };

  // ✏️ Editar usuario
  const editarUsuario = async (id) => {
    const nombre = prompt("Nuevo nombre:");
    const email = prompt("Nuevo email:");
    const rol = prompt("Nuevo rol (usuario/admin):", "usuario");
    const password = prompt("Nueva contraseña (opcional):");

    try {
      const payload = {
        nombre,
        email,
        rol: rol?.toLowerCase() // 👈 normalizar rol
      };
      if (password) payload.password = password;

      await API.put(`/usuarios/${id}`, payload);
      alert("✏️ Usuario actualizado");
      cargarUsuarios();
    } catch (err) {
      console.error(err.response?.data || err);
      alert("❌ Error al editar usuario");
    }
  };

  // 🗑️ Eliminar usuario
  const eliminarUsuario = async (id) => {
    if (!window.confirm("¿Seguro que quieres eliminar este usuario?")) return;
    try {
      await API.delete(`/usuarios/${id}`);
      alert("🗑️ Usuario eliminado");
      cargarUsuarios();
    } catch (err) {
      console.error(err.response?.data || err);
      alert("❌ Error al eliminar usuario");
    }
  };

  // 📜 Emitir certificado y descargar archivo .p12
  const emitirCertificado = async () => {
    const usuario_id = prompt("ID del usuario:");
    const password = prompt("Contraseña para proteger el certificado:");

    if (!usuario_id || !password) return;

    try {
      const res = await API.post(
        "/certificados/",
        { usuario_id, password },
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `cert_usuario_${usuario_id}.p12`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      alert("📜 Certificado emitido y descargado");
      cargarCertificados();
    } catch (err) {
      console.error(err.response?.data || err);
      alert("❌ Error al emitir certificado");
    }
  };

  // 🚫 Revocar certificado
  const revocarCertificado = async (id) => {
    try {
      await API.put(`/certificados/${id}/revocar`);
      alert("🚫 Certificado revocado");
      cargarCertificados();
    } catch (err) {
      console.error(err.response?.data || err);
      alert("❌ Error al revocar certificado");
    }
  };

  // 🗑️ Eliminar certificado
  const eliminarCertificado = async (id) => {
    if (!window.confirm("¿Seguro que quieres eliminar este certificado?")) return;
    try {
      await API.delete(`/certificados/${id}`);
      alert("🗑️ Certificado eliminado");
      cargarCertificados();
    } catch (err) {
      console.error(err.response?.data || err);
      alert("❌ Error al eliminar certificado");
    }
  };

  return (
    <div className="admin-panel">
      <h2>Gestión de Usuarios</h2>
      <button onClick={crearUsuario}>Crear Usuario</button>
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Nombre</th><th>Email</th><th>Rol</th><th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.nombre}</td>
              <td>{u.email}</td>
              <td>{u.rol}</td>
              <td>
                <button onClick={() => editarUsuario(u.id)}>Editar</button>
                <button onClick={() => eliminarUsuario(u.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Gestión de Certificados</h2>
      <button onClick={emitirCertificado}>Emitir Certificado</button>
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Usuario</th><th>Expira</th><th>Válido</th><th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {certificados.map(c => (
            <tr key={c.id}>
              <td>{c.id}</td>
              <td>{c.usuario_id}</td>
              <td>{c.expira || "N/A"}</td>
              <td>{c.valido ? "Sí" : "No"}</td>
              <td>
                <button onClick={() => revocarCertificado(c.id)}>Revocar</button>
                <button onClick={() => eliminarCertificado(c.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminPanel;
