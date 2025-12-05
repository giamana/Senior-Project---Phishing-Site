
// src/App.jsx
import React from "react";
import { Routes, Route, useLocation, Navigate } from "react-router-dom";
import "./App.css";

import NavBar from "./components/NavBar";

import HomePage from "./views/HomePage";
import AboutPage from "./views/AboutPage";
import LoginPage from "./views/LoginPage";
import SignUpPage from "./views/SignUpPage";

import EmployeeDashboard from "./views/EmployeeDashboard";
import EmployerDashboard from "./views/EmployerDashboard";
import DeveloperDashboard from "./views/DeveloperDashboard";

// Optional pages (create placeholders if missing)
import PlatformPage from "./views/PlatformPage";
import ResourcesPage from "./views/ResourcesPage";
import WatchDemoPage from "./views/WatchDemoPage";
import HighestRisks from "./views/HighestRisks";
import LowestRisks from "./views/LowestRisks";
import EmployeeDetailPage from "./views/EmployeeDetailPage";

import ProtectedRoute from "./auth/ProtectedRoute";

const norm = (v) => (typeof v === "string" ? v.toLowerCase() : "");
const roleHome = (role) =>
  norm(role) === "employer" ? "/employer" :
  norm(role) === "developer" ? "/dev" : "/employee";

/** Landing route: if logged in, go to their dashboard; else HomePage */
function RoleLanding() {
  let role = null;
  try {
    const lsUser = JSON.parse(localStorage.getItem("user") || "{}");
    role = lsUser?.role || localStorage.getItem("role");
  } catch {
    role = localStorage.getItem("role");
  }
  const token = localStorage.getItem("token");

  if (token && role) {
    return <Navigate to={roleHome(role)} replace />;
  }
  return <HomePage />;
}

/** NavBar that hides on /login and /signUp, and is full-width on platform/dashboard pages */
function NavBarWrapper() {
  const location = useLocation();
  if (location.pathname === "/login" || location.pathname === "/signUp") {
    return null;
  }

  const defaultProps = {
    className:
      "shadow-md bg-[#181818]/75 fixed top-0 z-20 w-3/5 justify-center items-center left-1/2 transform -translate-x-1/2",
  };

  const platformProps = {
    className:
      "shadow-md bg-[#404143] fixed top-0 z-20 w-full justify-center items-center",
  };

  const onPlatform =
    location.pathname === "/platform" ||
    location.pathname === "/resources" ||
    location.pathname === "/highest" ||
    location.pathname === "/lowest" ||
    location.pathname === "/demo" ||
    location.pathname.startsWith("/platform") ||
    location.pathname.startsWith("/employees") ||
    location.pathname.startsWith("/employee") ||
    location.pathname.startsWith("/employer") ||
    location.pathname.startsWith("/dev");

  return <NavBar {...(onPlatform ? platformProps : defaultProps)} hideButton={onPlatform} />;
}

export default function App() {
  return (
    <>
      {/* NavBar relies on useLocation, so it must be inside the single top-level Router (provided by main.jsx) */}
      <NavBarWrapper />
      <Routes>
        <Route path="/" element={<RoleLanding />} />
        <Route path="/about" element={<AboutPage />} />

        {/* Auth */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signUp" element={<SignUpPage />} />

        {/* Dashboards (role-protected) */}
        <Route
          path="/employee"
          element={
            <ProtectedRoute allow={["employee"]}>
              <EmployeeDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/employer"
          element={
            <ProtectedRoute allow={["employer"]}>
              <EmployerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dev"
          element={
            <ProtectedRoute allow={["developer"]}>
              <DeveloperDashboard />
            </ProtectedRoute>
          }
        />

        {/* Optional pages */}
        <Route path="/platform" element={<PlatformPage />} />
        <Route path="/resources" element={<ResourcesPage />} />
        <Route path="/demo" element={<WatchDemoPage />} />
        <Route path="/highest" element={<HighestRisks />} />
        <Route path="/lowest" element={<LowestRisks />} />
        <Route
          path="/employees/:id"
          element={
            <ProtectedRoute allow={["employer", "developer"]}>
              <EmployeeDetailPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}
