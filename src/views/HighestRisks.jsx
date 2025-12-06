
import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet } from "../api/client";

const getEmployerId = () =>
  localStorage.getItem("saas_employer_id") || localStorage.getItem("employerId");

const getRateValue = (employee, rateKey) => {
  const value = employee?.metrics?.[rateKey];
  return typeof value === "number" ? value : 0;
};

const getScoreValue = (employee) =>
  typeof employee?.score === "number" ? employee.score : 0;

const getFailureCount = (employee) => {
  const total = employee?.metrics?.total_responses;
  if (typeof total !== "number" || total <= 0) return 0;
  return Math.round(getRateValue(employee, "click_rate") * total);
};

function HighestRisks() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const employerId = getEmployerId();
        const query = employerId ? `?employerId=${employerId}` : "";
        const data = await apiGet(`/api/employees${query}`);
        setEmployees(data.employees || []);
        setError("");
      } catch (err) {
        setError(err?.message || "Failed to load employees.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const highestRiskEmployees = useMemo(() => {
    if (!Array.isArray(employees)) return [];
    return [...employees].sort((a, b) => {
      const scoreDiff = getScoreValue(a) - getScoreValue(b); // lower score = higher risk
      if (scoreDiff !== 0) return scoreDiff;
      return getRateValue(b, "click_rate") - getRateValue(a, "click_rate");
    });
  }, [employees]);

  return (
    <div className="min-h-screen bg-gray-50 pt-24 pb-12 px-6">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-sm text-gray-500">Risk Overview</p>
            <h1 className="text-3xl font-bold text-gray-900">Highest Risk Employees</h1>
            <p className="text-sm text-gray-500 mt-1">
              Full list ranked by security score, with click rate as a tiebreaker.
            </p>
          </div>
          <Link
            to="/platform"
            className="text-sm font-semibold text-indigo-600 hover:underline"
          >
            Back to dashboard
          </Link>
        </div>

        <div className="bg-white border border-gray-200 rounded-xl shadow-sm">
          <div className="grid grid-cols-[1.5fr_1fr_0.7fr] bg-gray-100 p-3 rounded-t-xl font-semibold text-gray-700">
            <p>Employee Email</p>
            <p>Full Name</p>
            <p className="text-center">Failures</p>
          </div>
          <ul className="divide-y divide-gray-200">
            {loading && (
              <li className="p-3 text-sm text-gray-500">Loading employees...</li>
            )}
            {error && !loading && (
              <li className="p-3 text-sm text-red-600">{error}</li>
            )}
            {!loading && !error && highestRiskEmployees.length === 0 && (
              <li className="p-3 text-sm text-gray-500">No employees available.</li>
            )}
            {!loading &&
              !error &&
              highestRiskEmployees.map((emp, i) => {
                const failures = getFailureCount(emp);
                return (
                  <li
                    key={emp?.id ?? `high-${i}`}
                    className={`grid grid-cols-[1.5fr_1fr_0.7fr] items-center p-3 hover:bg-gray-50 transition-all duration-150 ${
                      i % 2 === 0 ? "bg-white" : "bg-gray-50"
                    }`}
                  >
                    <p className="text-xs text-gray-700">{emp?.email ?? "—"}</p>
                    <p className="text-xs font-medium text-gray-900">{emp?.name ?? "—"}</p>
                    <p className="text-xs text-gray-700 text-center">{failures}</p>
                  </li>
                );
              })}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default HighestRisks;
