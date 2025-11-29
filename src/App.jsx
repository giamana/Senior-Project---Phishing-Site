// src/App.jsx
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import AboutPage from "./views/AboutPage";
import LoginPage from "./views/LoginPage";
import SignUpPage from "./views/SignUpPage";
import EmployerDashboard from "./views/EmployerDashboard";
import EmployeeDashboard from "./views/EmployeeDashboard";
import DeveloperDashboard from "./views/DeveloperDashboard";
import ProtectedRoute from "./auth/ProtectedRoute";

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<AboutPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signUp" element={<SignUpPage />} />

        <Route
          path="/employee"
          element={
            <ProtectedRoute allowedRoles={["employee"]}>
              <EmployeeDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/employer"
          element={
            <ProtectedRoute allowedRoles={["employer"]}>
              <EmployerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dev"
          element={
            <ProtectedRoute allowedRoles={["developer"]}>
              <DeveloperDashboard />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<p className="p-8">Page not found</p>} />
      </Routes>
    </div>
  );
}

export default App;
