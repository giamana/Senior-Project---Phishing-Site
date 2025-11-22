import React, { useEffect, useRef } from "react";
import ApexCharts from "apexcharts";

function PlatformPage() {
  const chartRef = useRef(null);

  useEffect(() => {
    const chartConfig = {
      series: [
        {
          name: "Sales",
          data: [50, 40, 300, 320, 500, 350, 200, 230, 500],
        },
      ],
      chart: {
        type: "line",
        height: 240,
        toolbar: {
          show: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      colors: ["#020617"],
      stroke: {
        lineCap: "round",
        curve: "smooth",
      },
      markers: {
        size: 0,
      },
      xaxis: {
        categories: [
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
        labels: {
          style: {
            colors: "#616161",
            fontSize: "12px",
            fontFamily: "inherit",
            fontWeight: 400,
          },
        },
        axisTicks: { show: false },
        axisBorder: { show: false },
      },
      yaxis: {
        labels: {
          style: {
            colors: "#616161",
            fontSize: "12px",
            fontFamily: "inherit",
            fontWeight: 400,
          },
        },
      },
      grid: {
        show: true,
        borderColor: "#dddddd",
        strokeDashArray: 5,
        xaxis: { lines: { show: true } },
        padding: { top: 5, right: 20 },
      },
      fill: { opacity: 0.8 },
      tooltip: { theme: "dark" },
    };

    const chart = new ApexCharts(chartRef.current, chartConfig);
    chart.render();

    return () => chart.destroy(); // cleanup on unmount
  }, []);

  return (
    <div className="flex">
        <div className="w-1/5 h-screen bg-gray-100 p-8 flex flex-col justify-between border-r border-gray-200">

        <div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2 mt-20">Your Stats</h2>
          <ul className="space-y-3 text-gray-600 font-medium">
            <li className="p-2 rounded-lg hover:bg-gray-200 hover:text-gray-900 transition-all duration-200 cursor-pointer">
              Click Rate
            </li>
            <li className="p-2 rounded-lg hover:bg-gray-200 hover:text-gray-900 transition-all duration-200 cursor-pointer">
              Report Rate
            </li>
            <li className="p-2 rounded-lg hover:bg-gray-200 hover:text-gray-900 transition-all duration-200 cursor-pointer">
              Accuracy Rate
            </li>
            <li className="p-2 rounded-lg hover:bg-gray-200 hover:text-gray-900 transition-all duration-200 cursor-pointer">
              Overall Score
            </li>
          </ul>
        </div>

        <ul className="space-y-3 text-gray-600 font-medium">
          <li className="p-2 rounded-lg hover:bg-gray-200 hover:text-gray-900 transition-all duration-200 cursor-pointer">
            Help Information
          </li>
          <li className="p-2 rounded-lg text-red-600 hover:bg-red-100 hover:text-red-700 transition-all duration-200 cursor-pointer">
            Logout
          </li>
        </ul>
      </div>


      <div className="flex w-3/4 flex-col justify-start">
        <div className="flex justify-between items-start mb-8 mt-25 ml-7">
            <div>
              <p className="text-sm text-gray-500">Your dashboard</p>
              <h1 className="text-4xl font-bold text-gray-800 mt-1">
                Hi, <span className="text-gray-700">NAME</span>
              </h1>
            </div>
            <p className="text-sm text-gray-500 max-w-sm">
              Welcome to your dashboard! Here you can review your team’s simulator stats and performance metrics.
            </p>
          </div>

        <div className="flex justify-center items-start gap-6 mt-12 w-full">
            <div className="bg-white border border-gray-300 p-6 rounded-lg shadow w-1/4 flex flex-col items-center">
                <h2 className="text-xl font-semibold">Report Rate</h2>
                <p className="mt-2 text-gray-600 text-2xl">3</p>
            </div>

            <div className="bg-white border border-gray-300 p-6 rounded-lg shadow w-1/4 flex flex-col items-center">
                <h2 className="text-xl font-semibold text-red-400">Simulation Failed</h2>
                <p className="mt-2 text-gray-600 text-2xl">5</p>
            </div>

            <div className="bg-white border border-gray-300 p-6 rounded-lg shadow w-1/4 flex flex-col items-center">
                <h2 className="text-xl font-semibold">Simulations Sent</h2>
                <p className="mt-2 text-gray-600 text-2xl">2</p>
            </div>
        </div>


        <div className="">
          <div className="relative flex flex-col rounded-xl bg-white bg-clip-border text-gray-700 mt-10 border border-gray-300 w-3/4 ml-40">
            <div className="relative mx-4 mt-4 flex flex-col gap-4 overflow-hidden rounded-none bg-transparent bg-clip-border text-gray-700 border border-gray-100 md:flex-row md:items-center">
              <div className="w-max rounded-lg bg-white p-5 text-white">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0l-5.571 3-5.571-3"
                  />
              </div>
              <div>
                <h6 className="block font-sans text-base font-semibold leading-relaxed tracking-normal text-blue-gray-900 antialiased">
                  Click Rate
                </h6>
              </div>
            </div>
            <div className="pt-6 px-2 pb-0">
              <div ref={chartRef}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlatformPage;
