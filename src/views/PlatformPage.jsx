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
        <div className="w-1/5 h-screen bg-[#C0C0C0] p-6 flex flex-col mt-10">
            <h2 className="text-lg font-semibold mt-10">Your stats:</h2>
            <ul className="space-y-4 text-gray-700">
            <li>Click rate</li>
            <li>Report rate</li>
            <li>Accuracy rate</li>
            <li>Overall score</li>
            </ul>
        </div>

      <div className="flex w-3/4 flex-col justify-start">
        <p className="mt-25 mx-5">Your Dashboard</p>
        <h1 className="text-7xl mx-5">Hi Gianna</h1>

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
