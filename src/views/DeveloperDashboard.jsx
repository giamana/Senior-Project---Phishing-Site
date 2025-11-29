// src/views/DeveloperDashboard.jsx
import React, { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthProvider";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function DeveloperDashboard() {
  const { authFetch } = useAuth();
  const [stats, setStats] = useState(null);
  const [companies, setCompanies] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const s = await authFetch(`${API_URL}/dev/summary`);
        const c = await authFetch(`${API_URL}/dev/companies`);
        if (!s.ok || !c.ok) throw new Error("Failed to load data");
        setStats(await s.json());
        setCompanies(await c.json());
      } catch (err) {
        setError(err.message);
      }
    })();
  }, [authFetch]);

  return (
    <div className="p-8">
      <h2 className="text-3xl font-bold mb-4">Developer Dashboard</h2>
      {error && <p className="text-red-600 mb-4">{error}</p>}

      {stats && (
        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="bg-white border p-6 rounded shadow">
            <b>Total Companies:</b> {stats.company_count}
          </div>
          <div className="bg-white border p-6 rounded shadow">
            <b>Total Employees:</b> {stats.employee_count}
          </div>
          <div className="bg-white border p-6 rounded shadow">
            <b>Total Clicks:</b> {stats.total_clicks}
          </div>
        </div>
      )}

      <h3 className="text-xl font-semibold mb-2">Companies</h3>
      <ul className="bg-white border rounded p-4">
        {companies.map((c) => (
          <li key={c.id} className="py-2 border-b last:border-b-0">
            <b>{c.name}</b> — Employees: {c.employee_count}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DeveloperDashboard;
