import React, { useEffect, useRef } from "react";
import ApexCharts from "apexcharts";

function SummaryPage() {
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
    <div className="min-h-screen bg-white flex flex-col">
      <main className="flex-1 flex justify-center items-start w-full mt-15">
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
            <li className="p-2 rounded-lg hover:bg-gray-200 hover:text-gray-900 transition-all duration-200 cursor-pointer">
              Help Information
            </li>
            <li className="p-2 rounded-lg text-red-600 hover:bg-red-100 hover:text-red-700 transition-all duration-200 cursor-pointer">
              Logout
            </li>
          </ul>
        </div>

      
        <div className="ml-[22%] justify-start flex-1 flex flex-col mt-10 mx-10">
          <div className="flex justify-between items-start mb-8">
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

          {/* <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
            <div className="bg-white rounded-2xl shadow-sm p-6 text-center">
              <h2 className="text-gray-600 text-sm font-semibold mb-2">Click Rate</h2>
              <p className="text-3xl font-bold text-gray-800">2</p>
            </div>
            <div className="bg-white rounded-2xl shadow-sm p-6 text-center">
              <h2 className="text-gray-600 text-sm font-semibold mb-2">Report Rate</h2>
              <p className="text-3xl font-bold text-gray-800">2</p>
            </div>
            <div className="bg-white rounded-2xl shadow-sm p-6 text-center">
              <h2 className="text-red-600 text-sm font-semibold mb-2">Tests Failed</h2>
              <p className="text-3xl font-bold text-gray-800">0</p>
            </div>
          </div> */}

          <div className="">
          <div className="relative flex flex-col rounded-xl bg-neutral-100 bg-clip-border text-gray-700 mb-10 border border-gray-300 w-3/4 ml-20">
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
                  Overall Performance
                </h6>
              </div>
            </div>
            <div className="pt-6 px-2 pb-0">
              <div ref={chartRef}></div>
            </div>
          </div>
        </div>

        <div className="flex flex-row">
          <div class="w-full max-w-lg p-4  border border-gray-200 rounded-lg shadow-sm sm:p-8 bg-neutral-100 ">
              <div class="flex items-center justify-between mb-4">
                  <h5 class="text-xl font-bold leading-none text-gray-900 ">Highest Risks</h5>
                  <a href="#" class="text-sm font-medium text-blue-600 hover:underline">
                      View all
                  </a>
            </div>
           <div className="w-full">
              <hr className="text-neutral-300"/>
              <div className="grid grid-cols-[1.5fr_1fr_0.7fr] bg-gray-100 p-3 rounded-t-lg font-semibold text-gray-700">
                <p >Employee Email</p>
                <p>Full Name</p>
                <p>Failures</p>
              </div>

              <ul role="list" className="divide-y divide-gray-200">
                <li className="grid grid-cols-[1.5fr_1fr_0.7fr] items-center bg-white p-3 hover:bg-gray-50 transition-all duration-150 border-y-1 border-neutral-300">
                  <p className="text-xs text-gray-700">email@windster.com</p>
                  <p className="text-xs font-medium text-gray-900">Neil Sims</p>
                  <p className="text-xs text-gray-700 mx-5">5</p>
                </li>
                <li className="grid grid-cols-[1.5fr_1fr_0.7fr] items-center bg-neutral-100 p-3 hover:bg-gray-50 transition-all duration-150 border-y border-neutral-300">
                  <p className="text-xs text-gray-700">emily.hart@bloomwhimsy.com</p>
                  <p className="text-xs font-medium text-gray-900">Emily Hart</p>
                  <p className="text-xs text-gray-700 mx-5">2</p>
                </li>

                <li className="grid grid-cols-[1.5fr_1fr_0.7fr] items-center bg-white p-3 hover:bg-gray-50 transition-all duration-150 border-y border-neutral-300">
                  <p className="text-xs text-gray-700">lucas.miller@windster.com</p>
                  <p className="text-xs font-medium text-gray-900">Lucas Miller</p>
                  <p className="text-xs text-gray-700 mx-5">7</p>
                </li>

                <li className="grid grid-cols-[1.5fr_1fr_0.7fr] items-center bg-neutral-100 p-3 hover:bg-gray-50 transition-all duration-150 border-y border-neutral-300">
                  <p className="text-xs text-gray-700">ava.jameson@auroratech.io</p>
                  <p className="text-xs font-medium text-gray-900">Ava Jameson</p>
                  <p className="text-xs text-gray-700 mx-5">3</p>
                </li>

                <li className="grid grid-cols-[1.5fr_1fr_0.7fr] items-center bg-white p-3 hover:bg-gray-50 transition-all duration-150 border-y border-neutral-300">
                  <p className="text-xs text-gray-700">noah.smith@gmail.com</p>
                  <p className="text-xs font-medium text-gray-900">Noah Smith</p>
                  <p className="text-xs text-gray-700 mx-5">1</p>
                </li>
              </ul>
            </div>
        </div>


        <div class="w-full max-w-lg p-4  border border-gray-200 rounded-lg shadow-sm sm:p-8 bg-neutral-100 mx-10">
                <div class="flex items-center justify-between mb-4">
                    <h5 class="text-xl font-bold leading-none text-gray-900 ">Lowest Risks</h5>
                    <a href="#" class="text-sm font-medium text-blue-600 hover:underline">
                        View all
                    </a>
              </div>
                    <div className="w-full">
          <hr className="text-neutral-300" />
          <div className="grid grid-cols-2 bg-gray-100 p-3 rounded-t-lg font-semibold text-gray-700 text-center">
            <p>Employee Email</p>
            <p>Full Name</p>
          </div>

          <ul role="list" className="divide-y divide-gray-200">
            <li className="grid grid-cols-2 items-center bg-white p-3 hover:bg-gray-50 transition-all duration-150 border-y border-neutral-300 text-center">
              <p className="text-xs text-gray-700">sophie.mendez@bloomwhimsy.com</p>
              <p className="text-xs font-medium text-gray-900">Sophie Mendez</p>
            </li>

            <li className="grid grid-cols-2 items-center bg-neutral-100 p-3 hover:bg-gray-50 transition-all duration-150 border-y border-neutral-300 text-center">
              <p className="text-xs text-gray-700">owen.clarke@windster.com</p>
              <p className="text-xs font-medium text-gray-900">Owen Clarke</p>
            </li>

            <li className="grid grid-cols-2 items-center bg-white p-3 hover:bg-gray-50 transition-all duration-150 border-y border-neutral-300 text-center">
              <p className="text-xs text-gray-700">mia.patel@auroratech.io</p>
              <p className="text-xs font-medium text-gray-900">Mia Patel</p>
            </li>

            <li className="grid grid-cols-2 items-center bg-neutral-100 p-3 hover:bg-gray-50 transition-all duration-150 border-y border-neutral-300 text-center">
              <p className="text-xs text-gray-700">julian.wright@bloomwhimsy.com</p>
              <p className="text-xs font-medium text-gray-900">Julian Wright</p>
            </li>

            <li className="grid grid-cols-2 items-center bg-white p-3 hover:bg-gray-50 transition-all duration-150 border-y border-neutral-300 text-center">
              <p className="text-xs text-gray-700">isabella.chen@gmail.com</p>
              <p className="text-xs font-medium text-gray-900">Isabella Chen</p>
            </li>
          </ul>
        </div>

        </div>

        </div>
        
        </div>
      </main>
    </div>
  );
}

export default SummaryPage;
