import React, { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const api = (p) => (API_URL.endsWith("/api") ? `${API_URL}${p}` : `${API_URL}/api${p}`);

export default function EmployeeDashboard() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const token = localStorage.getItem("token");

  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // For linking employee to employer
  const [employerId, setEmployerId] = useState("");
  const [employeeUserId, setEmployeeUserId] = useState(user?.id || "");

  const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };

  const loadStats = async () => {
    try {
      setLoading(true);
      const res = await fetch(api(`/employee/${user.id}/stats`), { headers });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to load stats");
      setStats(data);
      setError("");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user?.id && token) loadStats();
  }, [user?.id, token]);

  const linkToEmployer = async (e) => {
    e.preventDefault();
    if (!employerId || !employeeUserId) {
      setError("Employer ID and Employee User ID are required.");
      return;
    }
    try {
      const res = await fetch(api(`/employer/${employerId}/add-employee`), {
        method: "POST",
        headers,
        body: JSON.stringify({ employeeId: Number(employeeUserId) }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to link employee");
      setError("");
      alert(`Linked employee ${employeeUserId} to employer ${employerId}`);
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">
        Welcome, {user?.first_name} {user?.last_name || "Employee"}
   </h1>
    {user?.companyName && (
      <p className="text-gray-600">Company: {user.companyName}</p>
  )}

      {loading && <p className="mt-4">Loading your stats…</p>}
      {error && <p className="mt-4 text-red-500">{error}</p>}

      {!loading && !error && stats && (
        <div className="mt-4 space-y-1">
          <p>Emails Sent To You: <b>{stats.emailsSent ?? 0}</b></p>
          <p>URLs You Clicked: <b>{stats.urlsClicked ?? 0}</b></p>
        </div>
      )}

      {/* Form to link employee to employer */}
      <form onSubmit={linkToEmployer} className="mt-6 flex items-center gap-3">
        <input
          type="number"
          placeholder="Employer ID"
          value={employerId}
          onChange={(e) => setEmployerId(e.target.value)}
          className="border p-2 rounded w-48"
          required
        />
        <input
          type="number"
          placeholder="Your Employee User ID"
          value={employeeUserId}
          onChange={(e) => setEmployeeUserId(e.target.value)}
          className="border p-2 rounded w-48"
          required
        />
        <button type="submit" className="bg-black text-white px-4 py-2 rounded">
          Link to Employer
        </button>
      </form>
    </div>
  );
}
