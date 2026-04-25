import axios from "axios";

/**
 * Central API client
 * Automatically attaches JWT token if present
 */
const api = axios.create({
  baseURL: "http://localhost:8000/api", // adjust if needed
  headers: {
    "Content-Type": "application/json",
  },
});

/* -------------------------------
   Request Interceptor (JWT)
-------------------------------- */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/* -------------------------------
   Auth endpoints
-------------------------------- */
api.signup = (payload) => api.post("/auth/signup", payload);
api.login = (payload) => api.post("/auth/login", payload);

/* -------------------------------
   Domain endpoints
-------------------------------- */
api.listVendors = () => api.get("/vendor");
api.createVendor = (data) => api.post("/vendor", data);

api.createPO = (data) => api.post("/po", data);
api.getPO = (poNumber) => api.get(`/po/${poNumber}`);

api.askAgent = (prompt) =>
  api.post("/agent/ask", { prompt });

export default api;
