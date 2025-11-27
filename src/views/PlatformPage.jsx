import React, { useEffect, useRef, useState } from "react";
import ApexCharts from "apexcharts";
import { apiGet } from "../api/client";

const EMPLOYEE_CACHE_KEY = "saas_employee_cache";
const EMPLOYER_ID_KEY = "saas_employer_id";

function formatPercent(value) {
  if (value === undefined || value === null) return "0%";
  return `${Math.round(value * 100)}%`;
}

function SummaryPage() {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  const [employees, setEmployees] = useState([]);
  const [summary, setSummary] = useState(null);
  const [employerId, setEmployerId] = useState(
    localStorage.getItem(EMPLOYER_ID_KEY) || localStorage.getItem("employerId") || null
  );

  // Load employees & summary
  useEffect(() => {
    const bootstrap = async () => {
      const cached = localStorage.getItem(EMPLOYEE_CACHE_KEY);
      if (cached) {
        const parsed = JSON.parse(cached);
        setEmployees(parsed.employees || []);
        setSummary(parsed.summary || null);
      }

      fetchEmployees();
    };

    bootstrap();
  }, []);

  const fetchEmployees = async () => {
    const data = await apiGet(
      employerId ? `/api/employees?employerId=${employerId}` : "/api/employees"
    );

    setEmployees(data.employees || []);
    setSummary(data.summary || null);

    if (!employerId && data.employees?.length > 0) {
      const derived = data.employees[0].employer_id;
      if (derived) {
        localStorage.setItem(EMPLOYER_ID_KEY, String(derived));
        setEmployerId(String(derived));
      }
    }

    localStorage.setItem(
      EMPLOYEE_CACHE_KEY,
      JSON.stringify({ employees: data.employees || [], summary: data.summary || null })
    );
  };

  // Build the chart dynamically
  useEffect(() => {
    if (!chartRef.current || !summary) return;

    if (chartInstance.current) chartInstance.current.destroy();

    const data = [
      Math.round((summary.click_rate || 0) * 100),
      Math.round((summary.report_rate || 0) * 100),
      Math.round((summary.ignore_rate || 0) * 100),
    ];

    const chartConfig = {
      series: [{ name: "Rate", data }],
      chart: { type: "line", height: 240, toolbar: { show: false } },
      colors: ["#020617"],
      stroke: { lineCap: "round", curve: "smooth" },
      markers: { size: 0 },
      xaxis: { categories: ["Click", "Report", "Ignore"] },
      yaxis: { max: 100 },
      grid: { borderColor: "#ddd", strokeDashArray: 5 },
      tooltip: { theme: "dark" },
    };

    const chart = new ApexCharts(chartRef.current, chartConfig);
    chart.render();
    chartInstance.current = chart;

    return () => chart.destroy();
  }, [summary]);

  // Highest & Lowest risk employees
  const sortedByFailure = [...employees].sort((a, b) => (b.failures || 0) - (a.failures || 0));
  const highestRisk = sortedByFailure.slice(0, 5);
  const lowestRisk = [...employees].sort((a, b) => (a.failures || 0) - (b.failures || 0)).slice(0, 5);

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <main className="flex-1 flex">

        {/* Sidebar */}
        <div className="w-1/5 h-screen fixed bg-gray-100 p-8 flex flex-col justify-between border-r border-gray-200">
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2 mt-20">Summary Page</h2>
            <p className="text-sm text-gray-600 mt-5">
              Review your team's phishing performance including click behavior,
              reporting, and engagement over time.
            </p>
          </div>

          <ul className="space-y-3 text-gray-600 font-medium">
            <li className="hover:text-gray-900 cursor-pointer">Help Information</li>
            <li className="text-red-600 hover:text-red-700 cursor-pointer">Logout</li>
          </ul>
        </div>

        {/* Main Content */}
        <div className="ml-[22%] flex-1 flex flex-col mt-10 mx-10">

          {/* Header */}
          <div className="flex justify-between items-start mb-8">
            <div>
              <p className="text-sm text-gray-500">Your dashboard</p>
              <h1 className="text-4xl font-bold text-gray-800">
                Hi, <span className="text-gray-700">Admin</span>
              </h1>
            </div>
            <p className="text-sm text-gray-500 max-w-sm">
              Here’s a live overview of phishing performance across your workforce.
            </p>
          </div>

          {/* Summary Cards */}
          {summary && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
              <div className="bg-white rounded-2xl shadow-sm p-6 text-center">
                <h2 className="text-gray-600 text-sm font-semibold">Click Rate</h2>
                <p className="text-3xl font-bold">{formatPercent(summary.click_rate)}</p>
              </div>
              <div className="bg-white rounded-2xl shadow-sm p-6 text-center">
                <h2 className="text-gray-600 text-sm font-semibold">Report Rate</h2>
                <p className="text-3xl font-bold">{formatPercent(summary.report_rate)}</p>
              </div>
              <div className="bg-white rounded-2xl shadow-sm p-6 text-center">
                <h2 className="text-red-600 text-sm font-semibold">Risk Group</h2>
                <p className="text-3xl font-bold">{summary.grade}</p>
              </div>
            </div>
          )}

          {/* Chart */}
          <div className="bg-neutral-100 border border-gray-300 rounded-xl p-6 w-3/4 ml-20 mb-10">
            <h3 className="text-lg font-semibold mb-4">Overall Performance</h3>
            <div ref={chartRef}></div>
          </div>

          {/* Highest & Lowest Risk */}
          <div className="flex gap-8">

            {/* High Risk */}
            <div className="w-full max-w-lg p-6 border border-gray-200 rounded-lg bg-neutral-100">
              <h5 className="text-xl font-bold mb-2">Highest Risks</h5>
              <ul>
                {highestRisk.map((emp) => (
                  <li key={emp.id} className="grid grid-cols-3 bg-white p-2 my-1 text-xs">
                    <span>{emp.email}</span>
                    <span>{emp.name}</span>
                    <span>{emp.failures || 0}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Low Risk */}
            <div className="w-full max-w-lg p-6 border border-gray-200 rounded-lg bg-neutral-100">
              <h5 className="text-xl font-bold mb-2">Lowest Risks</h5>
              <ul>
                {lowestRisk.map((emp) => (
                  <li key={emp.id} className="grid grid-cols-2 bg-white p-2 my-1 text-xs text-center">
                    <span>{emp.email}</span>
                    <span>{emp.name}</span>
                  </li>
                ))}
              </ul>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}

export default SummaryPage;
