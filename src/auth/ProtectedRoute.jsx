// src/auth/ProtectedRoute.jsx
import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./AuthProvider";

/**
 * Guard protected routes.
 * Usage:
 *   <ProtectedRoute><Dashboard /></ProtectedRoute>
 */
export default function ProtectedRoute({ children }) {
  const location = useLocation();
  const auth = useAuth();

  const token = auth?.token || localStorage.getItem("token");

  // Not authenticated → go to login
  if (!token) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
}
