import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  withCredentials: true, // ✅ necesario si tu backend usa cookies o sesiones
  headers: {
    "Content-Type": "application/json", // ✅ cabecera por defecto
  },
});

// 📌 Interceptor para añadir el token JWT
API.interceptors.request.use(
  (req) => {
    const token = localStorage.getItem("token");
    if (token) {
      req.headers.Authorization = `Bearer ${token}`;
    }
    return req;
  },
  (error) => Promise.reject(error)
);

export default API;
