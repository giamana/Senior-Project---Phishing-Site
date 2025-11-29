// src/views/EmployerDashboard.jsx
import React, { useEffect, useState, useRef } from "react";
import { useAuth } from "../auth/AuthProvider";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function EmployerDashboard() {
  const { authFetch } = useAuth();
  const [stats, setStats] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [error, setError] = useState(null);
  const urlRef = useRef();

  useEffect(() => {
    (async () => {
      try {
        const s = await authFetch(`${API_URL}/employer/summary`);
        const e = await authFetch(`${API_URL}/employer/employees`);
        if (!s.ok || !e.ok) throw new Error("Failed to load data");
        setStats(await s.json());
        setEmployees(await e.json());
      } catch (err) {
        setError(err.message);
      }
    })();
  }, [authFetch]);

  const sendPhish = async () => {
    const url = urlRef.current.value.trim();
    try {
      const res = await authFetch(`${API_URL}/employer/campaigns`, {
        method: "POST",
        body: JSON.stringify({ url }),
      });
      if (!res.ok) throw new Error("Failed to create campaign");
      alert("Campaign created and emails sent!");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="p-8">
      <h2 className="text-3xl font-bold mb-4">Employer Dashboard</h2>
      {error && <p className="text-red-600 mb-4">{error}</p>}

      {stats && (
        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="bg-white border p-6 rounded shadow">
            <b>Total emails sent:</b> {stats.total_emails}
          </div>
          <div className="bg-white border p-6 rounded shadow">
            <b>Total clicks:</b> {stats.total_clicks}
          </div>
          <div className="bg-white border p-6 rounded shadow">
            <b>Employees:</b> {stats.employee_count}
          </div>
        </div>
      )}

      <div className="mb-6">
        <h3 className="text-xl font-semibold mb-2">Send phishing URL</h3>
        <div className="flex gap-3">
          <input
            ref={urlRef}
            type="url"
            placeholder="https://example.com/login"
            className="flex-1 p-2 rounded border"
          />
          <button
            onClick={sendPhish}
            className="px-4 py-2 bg-black text-white rounded"
          >
            Send
          </button>
        </div>
      </div>

      <h3 className="text-xl font-semibold mb-2">Employees</h3>
      <ul className="bg-white border rounded p-4">
        {employees.map((e) => (
          <li key={e.id} className="py-2 border-b last:border-b-0">
            <b>{e.name}</b> — {e.email} — Clicks: {e.clicks}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EmployerDashboard;
