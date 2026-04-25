import { Navigate, Outlet } from "react-router-dom";

export default function ProtectedRoute({ roles }) {
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user"));

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/menu" replace />;
  }

  return <Outlet />;
}
