
import React, { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const api = (p) => (API_URL.endsWith("/api") ? `${API_URL}${p}` : `${API_URL}/api${p}`);

export default function EmployerDashboard() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const token = localStorage.getItem("token");

  const [employees, setEmployees] = useState([]);
  const [totals, setTotals] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const [newEmployeeId, setNewEmployeeId] = useState("");
  const [templateId, setTemplateId] = useState(""); // use a developer-provided templateId
  const [sendingFor, setSendingFor] = useState(null);

  const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };

  const loadData = async () => {
    try {
      setLoading(true);
      const [empRes, totRes] = await Promise.all([
        fetch(api(`/employer/${user.id}/employees`), { headers }),
        fetch(api(`/employer/${user.id}/stats`), { headers }),
      ]);
      const [empData, totData] = await Promise.all([empRes.json(), totRes.json()]);
      if (!empRes.ok) throw new Error(empData.detail || "Failed to load employees");
      if (!totRes.ok) throw new Error(totData.detail || "Failed to load totals");
      setEmployees(empData.employees || []);
      setTotals(totData);
      setError("");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user?.id && token) loadData();
  }, [user?.id, token]);


  const addEmployee = async (e) => {
    e.preventDefault();
    if (!newEmployeeId) return;
    try {
      const res = await fetch(api(`/employer/${user.id}/add-employee`), {
        method: "POST",
        headers,
        body: JSON.stringify({ employeeId: Number(newEmployeeId) }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to add employee");
      setNewEmployeeId("");
      await loadData();
    } catch (e) {
      setError(e.message);
    }
  };

  const sendEmail = async (employeeId) => {
    if (!templateId) {
      setError("Please enter a templateId created by the Developer before sending.");
      return;
    }
    try {
      setSendingFor(employeeId);
      const res = await fetch(api(`/employer/${user.id}/send-email/${employeeId}`), {
        method: "POST",
        headers,
        body: JSON.stringify({ templateId: Number(templateId) }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to send email");
      // You can show the tracking URL if you wish
      console.log("Track URL:", data.trackUrl);
      await loadData();
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
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to delete employee");
      setEmployees((prev) => prev.filter((e) => e.id !== employeeId));
      await loadData();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="p-6">
            <h1 className="text-2xl font-bold">
        Welcome, {user?.first_name} {user?.last_name || "Employer"}
      </h1>
      {user?.companyName && (
        <p className="text-gray-600">Company: {user.companyName}</p>
      )}

      {loading && <p className="mt-4">Loading employees and totals…</p>}
      {error && <p className="mt-4 text-red-500">{error}</p>}

            {!loading && !error && totals && (
        <div className="mt-4">
          <p>Total Employees: <b>{totals.totalEmployees ?? 0}</b></p>
          <p>Total Emails Sent: <b>{totals.totalEmailsSent ?? 0}</b></p>
          <p>Total URLs Clicked: <b>{totals.totalUrlsClicked ?? 0}</b></p>
        </div>
      )}



      {/* Add employee by employee User.id */}
      <form onSubmit={addEmployee} className="mt-6 flex items-center gap-3">
        <input
          type="number"
          placeholder="Employee User ID"
          value={newEmployeeId}
          onChange={(e) => setNewEmployeeId(e.target.value)}
          className="border p-2 rounded w-48"
        />
        <button type="submit" className="bg-black text-white px-4 py-2 rounded">
          Add Employee
        </button>

        {/* Template ID used for sending emails */}
        <input
          type="number"
          placeholder="Template ID"
          value={templateId}
          onChange={(e) => setTemplateId(e.target.value)}
          className="border p-2 rounded w-40 ml-6"
        />
        <span className="text-sm text-gray-500">Use a template created by the Developer</span>
      </form>

      {/* Employees table */}
      <h2 className="text-xl mt-6">Employees</h2>
      <div className="mt-2 overflow-x-auto">
        <table className="w-full border">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 text-left">Name</th>
              <th className="p-2 text-left">Emails Sent</th>
              <th className="p-2 text-left">URLs Clicked</th>
              <th className="p-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {employees.length === 0 && (
              <tr><td className="p-3" colSpan={4}>No employees yet.</td></tr>
            )}
            {employees.map((emp) => (
              <tr key={emp.id} className="border-t">
               <td className="p-2">{emp.first_name} {emp.last_name}</td>
               <td className="p-2">{emp.emailsSent ?? 0}</td>
               <td className="p-2">{emp.urlsClicked ?? 0}</td>


                <td className="p-2 space-x-3">
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
    </div>
  );
}
