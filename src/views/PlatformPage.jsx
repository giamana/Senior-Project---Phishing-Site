import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet, apiPost } from "../api/client";

const EMPTY_FORM = { name: "", email: "", department: "" };
const SELECTED_TEMPLATES_KEY = "saas_selected_templates";
const EMPLOYEE_CACHE_KEY = "saas_employee_cache";
const AUTO_SIM_KEY = "saas_auto_sim_active";
const EMPLOYER_ID_KEY = "saas_employer_id";
const DEPARTMENTS = [
  "Aircraft Maintenance and Support",
  "At the Airport",
  "Corporate",
  "Customer Solutions",
  "Digital Technology",
  "Customer Service",
  "Finance",
  "Flight Attendant",
  "HR",
  "IT Support",
  "Pilot Operations",
];

const statusPillStyles = {
  "Security Champion": "bg-emerald-100 text-emerald-700",
  "At Risk": "bg-red-100 text-red-700",
  "On Track": "bg-blue-100 text-blue-800",
  Monitor: "bg-amber-100 text-amber-700",
};

function formatPercent(value) {
  if (value === undefined || value === null) return "0%";
  return `${Math.round(value * 100)}%`;
}

function PlatformPage() {
  const [employees, setEmployees] = useState([]);
  const [summary, setSummary] = useState(null);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplates, setSelectedTemplates] = useState([]);
  const [formData, setFormData] = useState(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [runningSimulation, setRunningSimulation] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [statusVariant, setStatusVariant] = useState("info");
  const [autoSimActive, setAutoSimActive] = useState(false);
  const [employerId, setEmployerId] = useState(
    localStorage.getItem(EMPLOYER_ID_KEY) || localStorage.getItem("employerId") || null
  );

  // ------------------- INITIALIZATION -------------------
  useEffect(() => {
    const bootstrap = async () => {
      const savedTemplates = localStorage.getItem(SELECTED_TEMPLATES_KEY);
      if (savedTemplates) {
        try {
          setSelectedTemplates(JSON.parse(savedTemplates));
        } catch (e) {
          console.warn("Unable to parse cached selected templates", e);
        }
      }
      const savedEmployees = localStorage.getItem(EMPLOYEE_CACHE_KEY);
      if (savedEmployees) {
        try {
          const cached = JSON.parse(savedEmployees);
          setEmployees(cached.employees || []);
          setSummary(cached.summary || null);
        } catch (e) {
          console.warn("Unable to parse cached employees", e);
        }
      }
      const savedAutoSim = localStorage.getItem(AUTO_SIM_KEY);
      if (savedAutoSim) setAutoSimActive(savedAutoSim === "true");

      try {
        await apiPost("/api/simulations/sweep", {});
      } catch (err) {
        console.warn("Unable to auto-mark ignored simulations", err);
      }
      fetchEmployees();
      fetchTemplates();
    };

    bootstrap();
  }, []);

  // ------------------- FETCHING DATA -------------------
  const fetchEmployees = async () => {
    try {
      const data = await apiGet(
        employerId ? `/api/employees?employerId=${employerId}` : "/api/employees"
      );
      setEmployees(data.employees || []);
      setSummary(data.summary || null);
      if (!employerId && data.employees && data.employees.length > 0) {
        const derived = data.employees[0].employer_id;
        if (derived !== undefined && derived !== null) {
          setEmployerId(String(derived));
          localStorage.setItem(EMPLOYER_ID_KEY, String(derived));
        }
      }
      localStorage.setItem(
        EMPLOYEE_CACHE_KEY,
        JSON.stringify({ employees: data.employees || [], summary: data.summary || null })
      );
    } catch (err) {
      setStatusVariant("error");
      setStatusMessage(`Failed to load employees: ${err.message}`);
    }
  };

  const fetchTemplates = async () => {
    try {
      const data = await apiGet("/api/templates");
      setTemplates(data.templates || []);
    } catch (err) {
      console.warn("Failed to load templates", err);
    }
  };

  // ------------------- HANDLERS -------------------
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAddEmployee = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await apiPost("/api/employees", { ...formData, employerId });
      setFormData(EMPTY_FORM);
      setStatusVariant("success");
      setStatusMessage("Employee added successfully.");
      fetchEmployees();
    } catch (err) {
      setStatusVariant("error");
      setStatusMessage(`Unable to add employee: ${err.message}`);
    } finally { setSubmitting(false); }
  };

  const toggleTemplate = (templateId) => {
    setSelectedTemplates((prev) => prev.includes(templateId) ? prev.filter((id) => id !== templateId) : [...prev, templateId]);
  };

  const handleSelectAll = () => setSelectedTemplates(templates.map((t) => t.id));
  const handleClearAll = () => setSelectedTemplates([]);

  const handleDeleteAllEmployees = async () => {
    const confirmed = window.confirm("Delete all employees? This cannot be undone.");
    if (!confirmed) return;
    try {
      const effectiveEmployerId = employerId || (employees[0] && employees[0].employer_id);
      if (!effectiveEmployerId) { setStatusVariant("error"); setStatusMessage("Employer ID missing; cannot delete employees."); return; }
      const result = await apiPost("/api/employees/delete_all", { employerId: effectiveEmployerId });
      setEmployees([]); setSummary(null);
      localStorage.setItem(EMPLOYEE_CACHE_KEY, JSON.stringify({ employees: [], summary: null }));
      setStatusVariant("success"); setStatusMessage(`Deleted ${result.deleted || 0} employees.`);
    } catch (err) {
      setStatusVariant("error"); setStatusMessage(`Failed to delete employees: ${err.message}`);
    }
  };

  const handleRunSimulation = async ({ silent = false, auto = false } = {}) => {
    if (runningSimulation && !auto) return;
    if (!silent) setRunningSimulation(true);
    try {
      const response = await apiPost("/api/simulations/run", { templateIds: selectedTemplates });
      if (!silent) { setStatusVariant("success"); setStatusMessage(`Simulation queued for ${response.scheduled} employees.`); }
    } catch (err) {
      if (!silent) { setStatusVariant("error"); setStatusMessage(`Failed to run simulation: ${err.message}`); }
    } finally { if (!silent) setRunningSimulation(false); fetchEmployees(); }
  };

  const startAutoSim = () => setAutoSimActive(true);
  const stopAutoSim = () => setAutoSimActive(false);

  useEffect(() => { localStorage.setItem(SELECTED_TEMPLATES_KEY, JSON.stringify(selectedTemplates)); }, [selectedTemplates]);
  useEffect(() => {
    localStorage.setItem(AUTO_SIM_KEY, autoSimActive ? "true" : "false");
    if (!autoSimActive) return undefined;
    const intervalId = setInterval(() => { if (selectedTemplates.length > 0) handleRunSimulation({ silent: true, auto: true }); }, 60_000);
    return () => clearInterval(intervalId);
  }, [autoSimActive, selectedTemplates]);

  // ------------------- RENDER -------------------
  return (
    <div className="min-h-screen bg-gray-50 pt-24 pb-16 px-10 flex">
      {/* ------------------- SIDEBAR ------------------- */}
      <div className="w-1/5 h-screen fixed bg-gray-100 p-8 flex flex-col justify-between border-r border-gray-200 top-0 left-0">
        <div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2 mt-20">Summary Page</h2>
          <ul className="space-y-3 text-gray-600 font-medium">
            <li className="p-2 rounded-lg hover:bg-gray-200 hover:text-gray-900 transition-all duration-200 cursor-pointer">
              On this page, you can quickly see how each employee is performing in your phishing training. It highlights who has the highest and lowest fail rates, along with their click rate, accuracy, and overall performance. These metrics help you understand who’s improving, who needs support, and how your team is doing as a whole.
            </li>
          </ul>
        </div>
        <ul className="space-y-3 text-gray-600 font-medium">
          <li className="p-2 rounded-lg hover:bg-gray-200 hover:text-gray-900 transition-all duration-200 cursor-pointer">Help Information</li>
          <li className="p-2 rounded-lg text-red-600 hover:bg-red-100 hover:text-red-700 transition-all duration-200 cursor-pointer">Logout</li>
        </ul>
      </div>

      {/* ------------------- MAIN CONTENT ------------------- */}
      <div className="ml-[22%] flex-1 flex flex-col gap-10">
        {/* Status Bar */}
        {statusMessage && (
          <div className={`px-4 py-2 rounded-md text-sm ${
            statusVariant === "success" ? "bg-emerald-100 text-emerald-800" :
            statusVariant === "error" ? "bg-red-100 text-red-700" :
            "bg-blue-100 text-blue-800"
          }`}>
            {statusMessage}
          </div>
        )}

        {/* Top Stats */}
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
            <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
              <p className="text-gray-500 text-sm mb-1">Overall Score</p>
              <p className="text-3xl font-semibold">{summary.score}</p>
              <p className="text-green-600 text-sm mt-1">{summary.grade}</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
              <p className="text-gray-500 text-sm mb-1">Click Rate</p>
              <p className="text-3xl font-semibold">{formatPercent(summary.click_rate)}</p>
              <p className="text-gray-400 text-xs mt-1">Lower is better</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
              <p className="text-gray-500 text-sm mb-1">Report Rate</p>
              <p className="text-3xl font-semibold">{formatPercent(summary.report_rate)}</p>
              <p className="text-gray-400 text-xs mt-1">Goal: 60%+</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
              <p className="text-gray-500 text-sm mb-1">Ignore Rate</p>
              <p className="text-3xl font-semibold">{formatPercent(summary.ignore_rate)}</p>
              <p className="text-gray-400 text-xs mt-1">Employees who stayed vigilant</p>
            </div>
          </div>
        )}

        {/* Employees Table */}
        <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm mb-10">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Employee Performance</h2>
            <div className="flex items-center gap-3 text-sm text-gray-500">
              <span>{employees.length} enrolled</span>
              <button type="button" className="text-red-600 hover:underline font-semibold" onClick={handleDeleteAllEmployees} disabled={employees.length === 0}>
                Delete all
              </button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="text-left text-gray-500 uppercase border-b">
                <tr>
                  <th className="py-3">Name</th>
                  <th className="py-3">Department</th>
                  <th className="py-3">Status</th>
                  <th className="py-3">Score</th>
                  <th className="py-3">Click</th>
                  <th className="py-3">Report</th>
                  <th className="py-3">Ignore</th>
                </tr>
              </thead>
              <tbody>
                {employees.map((employee) => (
                  <tr key={employee.id} className="border-b last:border-none hover:bg-gray-50">
                    <td className="py-3 font-medium text-gray-900">
                      <Link to={`/employees/${employee.id}`} className="text-indigo-600 hover:underline">{employee.name}</Link>
                    </td>
                    <td className="py-3 text-gray-600">{employee.department || "—"}</td>
                    <td className="py-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusPillStyles[employee.status] || "bg-gray-100 text-gray-600"}`}>
                        {employee.status}
                      </span>
                    </td>
                    <td className="py-3 font-semibold">{employee.score}</td>
                    <td className="py-3">{formatPercent(employee.metrics.click_rate)}</td>
                    <td className="py-3">{formatPercent(employee.metrics.report_rate)}</td>
                    <td className="py-3">{formatPercent(employee.metrics.ignore_rate)}</td>
                  </tr>
                ))}
                {employees.length === 0 && (
                  <tr><td colSpan="7" className="text-center text-gray-500 py-6 text-sm">Add employees to begin tracking phishing performance.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Templates Section */}
        <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm mb-10">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Simulation Templates</h2>
            <div className="flex gap-3">
              <button onClick={handleSelectAll} className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200">Select All</button>
              <button onClick={handleClearAll} className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200">Clear All</button>
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {templates.map((template) => (
              <button
                key={template.id}
                onClick={() => toggleTemplate(template.id)}
                className={`p-3 border rounded-xl text-sm font-medium transition-all duration-150 ${
                  selectedTemplates.includes(template.id)
                    ? "bg-blue-600 text-white border-blue-600"
                    : "bg-white text-gray-700 border-gray-300 hover:bg-gray-100"
                }`}
              >
                {template.name}
              </button>
            ))}
          </div>

          <div className="mt-4 flex gap-3">
            <button
              onClick={() => handleRunSimulation()}
              disabled={selectedTemplates.length === 0 || runningSimulation}
              className={`px-4 py-2 rounded-lg text-white font-semibold transition-all duration-150 ${
                selectedTemplates.length === 0 || runningSimulation
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-green-600 hover:bg-green-700"
              }`}
            >
              {runningSimulation ? "Running Simulation..." : "Run Simulation"}
            </button>

            <button
              onClick={autoSimActive ? stopAutoSim : startAutoSim}
              className={`px-4 py-2 rounded-lg font-semibold transition-all duration-150 ${
                autoSimActive ? "bg-red-600 hover:bg-red-700 text-white" : "bg-blue-600 hover:bg-blue-700 text-white"
              }`}
            >
              {autoSimActive ? "Stop Auto Simulation" : "Start Auto Simulation"}
            </button>
          </div>
        </div>

        {/* Add Employee Form */}
        <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm mb-10 w-full max-w-md">
          <h2 className="text-xl font-semibold mb-4">Add Employee</h2>
          <form onSubmit={handleAddEmployee} className="space-y-4">
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              value={formData.name}
              onChange={handleInputChange}
              className="w-full border px-3 py-2 rounded-lg"
              required
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleInputChange}
              className="w-full border px-3 py-2 rounded-lg"
              required
            />
            <select
              name="department"
              value={formData.department}
              onChange={handleInputChange}
              className="w-full border px-3 py-2 rounded-lg"
              required
            >
              <option value="">Select Department</option>
              {DEPARTMENTS.map((dept) => (
                <option key={dept} value={dept}>
                  {dept}
                </option>
              ))}
            </select>
            <button
              type="submit"
              disabled={submitting}
              className={`w-full py-2 rounded-lg font-semibold text-white transition-all duration-150 ${
                submitting ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              {submitting ? "Adding..." : "Add Employee"}
            </button>
          </form>
        </div>

        {/* Highest / Lowest Risks Tables */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Highest Risk Employees</h2>
            <ul className="space-y-2">
              {employees
                .sort((a, b) => b.metrics.click_rate - a.metrics.click_rate)
                .slice(0, 5)
                .map((emp) => (
                  <li key={emp.id} className="flex justify-between">
                    <span>{emp.name}</span>
                    <span>{formatPercent(emp.metrics.click_rate)}</span>
                  </li>
                ))}
            </ul>
          </div>
          <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Lowest Risk Employees</h2>
            <ul className="space-y-2">
              {employees
                .sort((a, b) => a.metrics.click_rate - b.metrics.click_rate)
                .slice(0, 5)
                .map((emp) => (
                  <li key={emp.id} className="flex justify-between">
                    <span>{emp.name}</span>
                    <span>{formatPercent(emp.metrics.click_rate)}</span>
                  </li>
                ))}
            </ul>
          </div>
        </div>

      </div>
    </div>
  );
}

export default PlatformPage;
