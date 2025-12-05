
// src/auth/ProtectedRoute.jsx
import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./AuthProvider";

const norm = (v) => (typeof v === "string" ? v.toLowerCase() : "");
const roleHome = (role) => {
  switch (norm(role)) {
    case "employer": return "/employer";
    case "developer": return "/dev";
    case "employee":
    default: return "/employee";
  }
};

/**
 * Guard protected routes by role.
 * Usage:
 *   <ProtectedRoute allow={["employee"]}><EmployeeDashboard /></ProtectedRoute>
 *   <ProtectedRoute allow={["employer"]}><EmployerDashboard /></ProtectedRoute>
 *   <ProtectedRoute allow={["developer"]}><DeveloperDashboard /></ProtectedRoute>
 */
export default function ProtectedRoute({ children, allow = [] }) {
  const location = useLocation();
  const auth = useAuth();

  // Try context first, then localStorage fallback
  const token = auth?.token || localStorage.getItem("token");
  const role =
    auth?.role ||
    (JSON.parse(localStorage.getItem("user") || "{}")?.role) ||
    localStorage.getItem("role");

  // Not authenticated → go to login
  if (!token) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // Role restriction
  if (allow.length && !allow.map(norm).includes(norm(role))) {
    return <Navigate to={roleHome(role)} replace />;
  }

  return children;
}
