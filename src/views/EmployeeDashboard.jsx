// src/views/EmployeeDashboard.jsx
import React, { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthProvider";
import { useNavigate } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function EmployeeDashboard() {
  const { token, logout, isAuthenticated, authFetch } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated || !token) {
      navigate("/login");
      return;
    }

    const fetchStats = async () => {
      try {
        const response = await authFetch(`${API_URL}/employee/summary`); // use your actual endpoint
        if (response.status === 401) {
          logout();
          navigate("/login");
          return;
        }
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [token, isAuthenticated, logout, navigate, authFetch]);

  if (loading) return <p className="p-8 text-lg">Loading stats...</p>;
  if (error) return <p className="p-8 text-red-600">Error: {error}</p>;

  return (
    <div className="p-8">
      <h2 className="text-3xl font-bold mb-6">Employee Dashboard</h2>
      {stats ? (
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-white border p-6 rounded shadow">
            <b>Emails received:</b> {stats.emails_received}
          </div>
          <div className="bg-white border p-6 rounded shadow">
            <b>Clicks:</b> {stats.clicks}
          </div>
        </div>
      ) : (
        <p>No stats available.</p>
      )}
    </div>
  );
}

export default EmployeeDashboard;
