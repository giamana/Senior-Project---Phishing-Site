
import React, { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const api = (p) => (API_URL.endsWith("/api") ? `${API_URL}${p}` : `${API_URL}/api${p}`);

export default function DeveloperDashboard() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const token = localStorage.getItem("token");

  const [companies, setCompanies] = useState([]);
  const [globalStats, setGlobalStats] = useState(null);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplateId, setSelectedTemplateId] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [sendingFor, setSendingFor] = useState(null);

  const headersAuth = { Authorization: `Bearer ${token}` };
  const headersJson = { ...headersAuth, "Content-Type": "application/json" };

  const load = async () => {
    try {
      setLoading(true);
      const [compRes, globalRes] = await Promise.all([
        fetch(api(`/companies`), { headers: headersAuth }),
        fetch(api(`/stats/global`), { headers: headersAuth }),
      ]);
      const [compData, globalData] = await Promise.all([compRes.json(), globalRes.json()]);
      if (!compRes.ok) throw new Error(compData.detail || "Failed to load companies");
      if (!globalRes.ok) throw new Error(globalData.detail || "Failed to load global stats");
      setCompanies(compData.companies || []);
      setGlobalStats(globalData);
      setError("");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  // Optional: load templates the developer has created
  const loadTemplates = async () => {
    try {
      // If you add a GET /api/developer/templates endpoint, fetch it here.
      // For now, we keep it empty until implemented on backend.
      setTemplates((prev) => prev);
    } catch (e) {
      console.warn("Templates list not implemented yet:", e.message);
    }
  };

  useEffect(() => {
    if (token) {
      load();
      loadTemplates();
    }
  }, [token]);

  const createTemplate = async (e) => {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const name = form.get("name");
    const subject = form.get("subject");
    const body = form.get("body");
    try {
      const res = await fetch(api(`/developer/templates`), {
        method: "POST",
        headers: headersJson,
        body: JSON.stringify({ name, subject, body }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to create template");
      setTemplates((prev) => [...prev, { id: data.id, name }]);
      setSelectedTemplateId(String(data.id));
      e.currentTarget.reset();
    } catch (e) {
      setError(e.message);
    }
  };

  const sendEmail = async (employeeId) => {
    if (!selectedTemplateId) {
      setError("Select or create a template before sending.");
      return;
    }
    try {
      setSendingFor(employeeId);
      const res = await fetch(api(`/developer/send-email/${employeeId}`), {
        method: "POST",
        headers: headersJson,
        body: JSON.stringify({ templateId: Number(selectedTemplateId) }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to send email");
      console.log("Track URL:", data.trackUrl);
      await load();
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
      // Update UI optimistically
      setCompanies((prev) =>
        prev.map((c) => ({ ...c, employees: (c.employees || []).filter((e) => e.id !== employeeId) }))
      );
      await load();
    } catch (e) {
      setError(e.message);
    }
  };

  const deleteCompany = async (companyId) => {
    try {
      const res = await fetch(api(`/companies/${companyId}`), {
        method: "DELETE",
        headers: headersAuth,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to delete company");
      setCompanies((prev) => prev.filter((c) => c.id !== companyId));
      await load();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Welcome, {user?.name || "Developer"}</h1>

      {loading && <p className="mt-4">Loading companies & global stats…</p>}
      {error && <p className="mt-4 text-red-500">{error}</p>}

      {!loading && !error && globalStats && (
        <div className="mt-4 space-y-1">
          <p>Total Companies: <b>{globalStats.totalCompanies ?? 0}</b></p>
          <p>Total Employees: <b>{globalStats.totalEmployees ?? 0}</b></p>
          <p>Total Emails Sent: <b>{globalStats.totalEmailsSent ?? 0}</b></p>
          <p>Total URLs Clicked: <b>{globalStats.totalUrlsClicked ?? 0}</b></p>
        </div>
      )}

      {/* Template creator & selector */}
      <div className="mt-6 border rounded p-4">
        <h2 className="text-xl font-semibold">Email Templates</h2>

        <form onSubmit={createTemplate} className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-3">
          <input name="name" placeholder="Template Name" className="border p-2 rounded" required />
          <input name="subject" placeholder="Subject" className="border p-2 rounded" required />
          <input name="body" placeholder="Body" className="border p-2 rounded" required />
          <button type="submit" className="bg-black text-white px-4 py-2 rounded md:col-span-3">
            Create Template
          </button>
        </form>

        <div className="mt-4 flex items-center gap-3">
          <select
            value={selectedTemplateId}
            onChange={(e) => setSelectedTemplateId(e.target.value)}
            className="border p-2 rounded"
          >
            <option value="">Select a template…</option>
            {templates.map((t) => (
              <option key={t.id} value={t.id}>{t.name} (#{t.id})</option>
            ))}
          </select>
          <span className="text-sm text-gray-500">Selected template will be used for “Send” actions.</span>
        </div>
      </div>

      {/* Companies + employees */}
      <h2 className="text-xl mt-8">Companies</h2>
      {companies.length === 0 && <p className="mt-2">No companies found.</p>}

      {companies.map((company) => (
        <div key={company.id} className="border p-4 mt-4 rounded">
          <div className="flex justify-between items-start">
            <div>
              <p className="font-bold">{company.name}</p>
              <p>Employees: {company.employeesCount ?? (company.employees?.length || 0)}</p>
              <p>Emails Sent: {company.emailsSent ?? 0}</p>
              <p>URLs Clicked: {company.urlsClicked ?? 0}</p>
            </div>
            <button
              onClick={() => deleteCompany(company.id)}
              className="px-3 py-1 bg-red-600 text-white rounded"
            >
              Delete Company
            </button>
          </div>

          <h3 className="mt-4 font-medium">Employees</h3>
          {(!company.employees || company.employees.length === 0) && (
            <p className="mt-2 text-sm">No employees in this company.</p>
          )}

          <ul className="mt-2">
            {(company.employees || []).map((emp) => (
              <li key={emp.id} className="flex justify-between items-center border-b py-2">
                <div>
                  <div className="font-medium">{emp.name}</div>
                  <div className="text-sm">
                    Emails Sent: <b>{emp.emailsSent ?? 0}</b> &nbsp;|&nbsp;
                    URLs Clicked: <b>{emp.urlsClicked ?? 0}</b>
                  </div>
                </div>
                <div className="space-x-3">
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
                </div>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
