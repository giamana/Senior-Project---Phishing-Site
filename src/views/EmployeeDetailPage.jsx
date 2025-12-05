import React, { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const api = (p) => (API_URL.endsWith("/api") ? `${API_URL}${p}` : `${API_URL}/api${p}`);

export default function EmployerDashboard() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const token = localStorage.getItem("token");
  const employerId = user?.id;

  const [employees, setEmployees] = useState([]);
  const [stats, setStats] = useState(null);
  const [employeeIdToAdd, setEmployeeIdToAdd] = useState("");
  const [templateId, setTemplateId] = useState("");
  const [error, setError] = useState("");
  const [sendingFor, setSendingFor] = useState(null);

  const headersAuth = { Authorization: `Bearer ${token}` };
  const headersJson = { ...headersAuth, "Content-Type": "application/json" };

  const loadEmployees = async () => {
    try {
      const res = await fetch(api(`/employer/${employerId}/employees`), { headers: headersAuth });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to load employees");
      setEmployees(data.employees || []);
    } catch (e) {
      setError(e.message);
    }
  };

  const loadStats = async () => {
    try {
      const res = await fetch(api(`/employer/${employerId}/stats`), { headers: headersAuth });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to load stats");
      setStats(data);
    } catch (e) {
      setError(e.message);
    }
  };

  useEffect(() => {
    if (token && employerId) {
      loadEmployees();
      loadStats();
    }
  }, [token, employerId]);

  const handleAddEmployee = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(api(`/employer/${employerId}/add-employee`), {
        method: "POST",
        headers: headersJson,
        body: JSON.stringify({ employeeId: Number(employeeIdToAdd) }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to add employee");
      setEmployeeIdToAdd("");
      await loadEmployees();
    } catch (e) {
      setError(e.message);
    }
  };

  const sendEmail = async (employeeId) => {
    if (!templateId) {
      setError("Please enter a template ID first.");
      return;
    }
    try {
      setSendingFor(employeeId);
      const res = await fetch(api(`/employer/${employerId}/send-email/${employeeId}`), {
        method: "POST",
        headers: headersJson,
        body: JSON.stringify({ templateId: Number(templateId) }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to send email");
      await loadEmployees();
    } catch (e) {
      setError(e.message);
    } finally {
      setSendingFor(null);
    }
  };

  const deleteEmployee = async (employeeId) => {
    try {
      const res = await fetch(api(`/employees/${employeeId}`), {
        method: "DELETE",
        headers: headersAuth,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to delete employee");
      await loadEmployees();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Welcome, {user?.name || "Employer"}</h1>

      {error && <p className="mt-4 text-red-500">{error}</p>}

      {stats && (
        <div className="mt-4 space-y-1">
          <p>Total Emails Sent: <b>{stats.totalEmailsSent ?? 0}</b></p>
          <p>Total URLs Clicked: <b>{stats.totalUrlsClicked ?? 0}</b></p>
        </div>
      )}

      <form onSubmit={handleAddEmployee} className="mt-6 flex gap-3 items-center">
        <input
          type="number"
          placeholder="Employee User ID"
          value={employeeIdToAdd}
          onChange={(e) => setEmployeeIdToAdd(e.target.value)}
          className="border p-2 rounded w-48"
          required
        />
        <button type="submit" className="bg-black text-white px-4 py-2 rounded">
          Add Employee
        </button>
      </form>

      <div className="mt-4">
        <label className="block text-sm font-medium mb-1">Use a template created by the Developer</label>
        <input
          type="number"
          placeholder="Template ID"
          value={templateId}
          onChange={(e) => setTemplateId(e.target.value)}
          className="border p-2 rounded w-48"
        />
      </div>

      <h2 className="text-xl mt-8">Employees</h2>
      {employees.length === 0 && <p className="mt-2">No employees yet.</p>}

      <table className="mt-4 w-full border-collapse">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2 text-left">Name</th>
            <th className="border p-2 text-left">Emails Sent</th>
            <th className="border p-2 text-left">URLs Clicked</th>
            <th className="border p-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((emp) => (
            <tr key={emp.id}>
              <td className="p-2">{emp.first_name} {emp.last_name}</td>
              <td className="p-2">{emp.emailsSent ?? 0}</td>
              <td className="p-2">{emp.urlsClicked ?? 0}</td>

              <td className="border p-2 space-x-2">
                <button
                  onClick={() => sendEmail(emp.id)}
                  className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50"
                  disabled={sendingFor === emp.id}
                >
                  {sendingFor === emp.id ? "Sending…" : "Send"}
                </button>
                <button
                  onClick={() => deleteEmployee(emp.id)}
                  className="px-3 py-1 bg-red-600 text-white rounded"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
