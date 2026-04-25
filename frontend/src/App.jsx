import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";

import VendorsPage from "./pages/VendorsPage";
import MenuHome from "./pages/MenuHome";
import CreatePOPage from "./pages/CreatePOPage";
import PODashboardPage from "./pages/PODashboardPage";
import AgentPage from "./pages/AgentPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";

export default function App() {
  return (
    <Routes>

      {/* -------- PUBLIC -------- */}
      <Route path="/" element={<Navigate to="/signup" replace />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/login" element={<LoginPage />} />

      {/* -------- PROTECTED -------- */}
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          
          <Route path="/menu" element={<MenuHome />} />
          <Route path="/po-dashboard" element={<PODashboardPage />} />

          {/* ADMIN ONLY */}
          <Route element={<ProtectedRoute roles={["admin"]} />}>
            <Route path="/vendors" element={<VendorsPage />} />
            <Route path="/create-po" element={<CreatePOPage />} />
          </Route>

          {/* ADMIN + BUYER */}
          <Route element={<ProtectedRoute roles={["admin", "buyer"]} />}>
            <Route path="/agent" element={<AgentPage />} />
          </Route>

        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/signup" replace />} />
    </Routes>
  );
}
