import Footer from "../Components/Footer";
import Navbar from "../Components/Navbar";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#f7f5ef] text-neutral-900 overflow-x-hidden">
      <Navbar />

      {/* HERO SECTION */}
      <main
        id="home"
        className="mx-auto flex max-w-6xl flex-col gap-10 px-6 pb-16 pt-14 md:flex-row md:items-center md:justify-between"
      >
        {/* Left: text content */}
        <section className="max-w-xl space-y-6">
          <h1 className="text-4xl font-semibold leading-tight tracking-tight md:text-6xl">
            Activity Monitoring
            <br />
            <span className="relative inline-block">
              You Can Rely On
              <svg
                className="absolute -bottom-2 left-0 w-full h-1.5"
                viewBox="0 0 200 10"
              >
                <path
                  d="M0,5 Q50,10 100,5 T200,5"
                  stroke="#2e5c46"
                  strokeWidth="2"
                  fill="none"
                  strokeDasharray="5,3"
                />
              </svg>
            </span>
          </h1>

          <p className="text-base text-neutral-600 md:text-lg">
            Nagster tracks real keyboard, mouse and app activity, so you see
            actual work instead of fake screen time. Perfect for remote and
            hybrid teams.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <button
              className="relative rounded-full bg-[#2e5c46] px-6 py-3 text-sm font-medium text-white shadow-md hover:bg-[#244636] transition-all duration-300 hover:scale-105 hover:shadow-lg group"
              onClick={() => {
                window.location.href = "#download";
              }}
            >
              <span className="relative z-10">Download Agent</span>
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-emerald-600 to-emerald-800 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </button>

            <a
              href="#features"
              className="text-sm font-medium text-neutral-800 underline underline-offset-4 hover:text-[#2e5c46] transition-colors"
            >
              Learn how it works
            </a>
          </div>

          <p className="text-xs text-neutral-500 flex items-center gap-2">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            Runs quietly in the background, flags idle & suspicious patterns
            without interrupting employees.
          </p>
        </section>

        {/* Right: Enhanced animated dashboard */}
        <section className="relative w-full max-w-md md:max-w-lg">
          {/* Animated background elements */}
          <div className="absolute -left-6 top-6 w-12 h-12 rounded-full bg-emerald-300/20 blur-xl animate-pulse"></div>
          <div className="absolute -right-4 bottom-8 w-10 h-10 rounded-full bg-indigo-300/20 blur-xl animate-pulse delay-700"></div>
          <div className="absolute top-1/2 left-1/4 w-8 h-8 rounded-full bg-amber-300/15 blur-lg animate-pulse delay-1000"></div>

          {/* Main dashboard container */}
          <div className="relative bg-white/70 backdrop-blur-sm rounded-3xl p-4 shadow-2xl border border-white/80">
            {/* Dashboard header */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></div>
                <span className="text-xs font-semibold text-neutral-700">
                  LIVE DASHBOARD
                </span>
              </div>
              <div className="text-xs text-neutral-500">Real-time</div>
            </div>

            {/* Dashboard grid */}
            <div className="grid grid-cols-2 gap-4">
              {/* Active Users Card */}
              <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-800 to-emerald-600 p-4 text-emerald-50 shadow-lg home-float-slow">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-400 to-transparent"></div>
                <div className="flex items-center justify-between">
                  <span className="inline-flex items-center gap-2 rounded-full bg-emerald-900/40 px-3 py-1 text-xs">
                    <span className="relative flex h-2 w-2">
                      <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-300 opacity-75"></span>
                      <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-300"></span>
                    </span>
                    Live activity
                  </span>
                  <span className="text-xs font-semibold text-emerald-200 flex items-center">
                    +12%
                    <svg
                      className="w-4 h-4 ml-1"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </span>
                </div>
                <div className="mt-6">
                  <div className="text-2xl font-bold">18</div>
                  <div className="text-xs text-emerald-200/80 mt-1">
                    employees active
                  </div>
                  <div className="mt-4">
                    <div className="flex justify-between text-xs mb-1">
                      <span>Activity level</span>
                      <span>75%</span>
                    </div>
                    <div className="h-2 overflow-hidden rounded-full bg-emerald-900/60">
                      <div className="h-full w-3/4 rounded-full bg-gradient-to-r from-emerald-300 to-emerald-400 home-progress"></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Idle Alerts Card */}
              <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-300 to-violet-300 p-4 shadow-lg home-float-slower">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 to-transparent"></div>
                <div className="h-full flex flex-col justify-center items-center">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-slate-800">32</div>
                    <div className="text-xs font-semibold text-slate-700 mt-1">
                      Idle alerts
                    </div>
                    <div className="mt-4 w-16 h-16 mx-auto relative">
                      <div className="absolute inset-0 border-4 border-slate-800/20 rounded-full"></div>
                      <div className="absolute inset-2 border-4 border-slate-800 border-t-transparent rounded-full home-spin-slow"></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Productivity Overview */}
              <div className="col-span-2 rounded-2xl bg-gradient-to-r from-slate-900 to-emerald-900 p-5 text-slate-100 shadow-lg">
                <div className="flex flex-col md:flex-row md:items-center justify-between">
                  <div className="space-y-2">
                    <p className="text-xs uppercase tracking-[0.18em] text-emerald-300/90 font-semibold">
                      Today&apos;s summary
                    </p>
                    <p className="text-lg font-semibold">
                      Team productivity overview
                    </p>
                    <p className="text-xs text-slate-300/90">
                      Active • Idle • Suspicious minutes
                    </p>
                  </div>
                  <div className="mt-4 md:mt-0">
                    <div className="flex items-end gap-2">
                      {[65, 40, 85, 30, 55, 75].map((height, index) => (
                        <div
                          key={index}
                          className="w-3 rounded-t-lg bg-gradient-to-t from-emerald-400 to-emerald-300 home-grow"
                          style={{
                            height: `${height}%`,
                            animationDelay: `${index * 100}ms`,
                            maxHeight: "3.5rem",
                          }}
                        ></div>
                      ))}
                    </div>
                    <div className="flex justify-between mt-2 text-[10px] text-slate-400">
                      <span>Mon</span>
                      <span>Tue</span>
                      <span>Wed</span>
                      <span>Thu</span>
                      <span>Fri</span>
                      <span>Sat</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Avg Idle Time */}
              <div className="relative rounded-2xl bg-gradient-to-br from-sky-100 to-white p-5 shadow-lg home-float-slower">
                <div className="text-center">
                  <div className="text-xs font-semibold text-slate-600 mb-2">
                    Avg. idle time
                  </div>
                  <div className="relative w-20 h-20 mx-auto mb-3">
                    <svg
                      className="w-full h-full transform -rotate-90"
                      viewBox="0 0 36 36"
                    >
                      <path
                        d="M18 2.0845
                          a 15.9155 15.9155 0 0 1 0 31.831
                          a 15.9155 15.9155 0 0 1 0 -31.831"
                        fill="none"
                        stroke="#e2e8f0"
                        strokeWidth="3"
                      />
                      <path
                        d="M18 2.0845
                          a 15.9155 15.9155 0 0 1 0 31.831
                          a 15.9155 15.9155 0 0 1 0 -31.831"
                        fill="none"
                        stroke="#0ea5e9"
                        strokeWidth="3"
                        strokeDasharray="60, 100"
                        className="home-circle"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-xl font-bold text-slate-900">42</div>
                    </div>
                  </div>
                  <div className="text-xs text-slate-600">minutes</div>
                </div>
              </div>

              {/* Suspicious Activity */}
              <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-500 to-emerald-400 p-5 text-emerald-950 shadow-lg home-float-slow">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-600 to-transparent"></div>
                <div className="relative z-10">
                  <p className="text-xs uppercase tracking-[0.18em] text-emerald-950/70 font-semibold">
                    Suspicious activity
                  </p>
                  <p className="text-lg font-bold mt-1">3 sessions flagged</p>
                  <p className="text-xs mt-2">
                    Macro-like patterns & fake key spam detected.
                  </p>
                  <div className="mt-4 flex items-center">
                    <div className="flex -space-x-2">
                      {[1, 2, 3].map((i) => (
                        <div
                          key={i}
                          className="w-6 h-6 rounded-full bg-emerald-900/30 border border-emerald-800/50 flex items-center justify-center"
                        >
                          <span className="text-[10px] font-bold text-emerald-950">
                            !
                          </span>
                        </div>
                      ))}
                    </div>
                    <div className="ml-3 text-xs font-semibold bg-emerald-900/20 px-2 py-1 rounded-full">
                      Review needed
                    </div>
                  </div>
                </div>
                <div className="absolute bottom-0 right-0 w-16 h-16 bg-emerald-600/20 rounded-full -mb-6 -mr-6"></div>
              </div>
            </div>

            {/* Live indicator */}
            <div className="absolute -top-2 -right-2">
              <div className="relative">
                <div className="w-4 h-4 rounded-full bg-emerald-500 animate-ping"></div>
                <div className="absolute top-0 left-0 w-4 h-4 rounded-full bg-emerald-500"></div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* FEATURES SECTION */}
      <section id="features" className="mx-auto max-w-6xl px-6 pb-16 pt-4">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-semibold text-neutral-900">
            How Nagster Works
          </h2>
          <p className="mt-2 text-neutral-600 max-w-2xl mx-auto">
            Advanced activity monitoring that distinguishes real work from fake
            presence
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-3">
          <div className="group relative bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 to-emerald-300 rounded-t-2xl"></div>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg
                className="w-6 h-6 text-emerald-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-neutral-800 mb-2">
              Real activity only
            </h3>
            <p className="text-sm text-neutral-600">
              Tracks actual keyboard, mouse and active windows instead of just
              login time, so fake "online" doesn't work.
            </p>
          </div>

          <div className="group relative bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 to-emerald-300 rounded-t-2xl"></div>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg
                className="w-6 h-6 text-emerald-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-neutral-800 mb-2">
              Smart idle logic
            </h3>
            <p className="text-sm text-neutral-600">
              Ignores app loading or long processing so employees aren't marked
              idle while work is running.
            </p>
          </div>

          <div className="group relative bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 to-emerald-300 rounded-t-2xl"></div>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg
                className="w-6 h-6 text-emerald-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-neutral-800 mb-2">
              Clean dashboard
            </h3>
            <p className="text-sm text-neutral-600">
              Daily active, idle and suspicious minutes per employee in a
              simple, manager-friendly view.
            </p>
          </div>
        </div>
      </section>

      {/* DOWNLOAD SECTION */}
      <section
        id="download"
        className="mx-auto max-w-4xl rounded-3xl bg-gradient-to-r from-emerald-50 to-white px-6 py-12 shadow-xl md:px-10 mb-16"
      >
        <div className="text-center mb-8">
          <h2 className="text-3xl font-semibold tracking-tight text-neutral-900">
            Download Nagster Agent
          </h2>
          <p className="mt-3 max-w-2xl mx-auto text-neutral-600">
            Install the agent on each employee machine. It runs at startup and
            streams activity events to your Nagster backend.
          </p>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-center gap-6">
          <button
            className="group relative rounded-full bg-gradient-to-r from-[#2e5c46] to-emerald-700 px-8 py-4 text-sm font-medium text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 w-full md:w-auto"
            onClick={() => {
              const link = document.createElement("a");
              link.href = "/agent.exe"; 
              link.download = "agent.exe";
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
            }}
          >
            <div className="flex items-center justify-center gap-3">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
              <span>Download for Windows</span>
            </div>
            <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-24 h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent rounded-full opacity-0 group-hover:opacity-100 transition-opacity"></div>
          </button>

          <button
            className="group rounded-full border-2 border-neutral-300 bg-white px-8 py-4 text-sm font-medium text-neutral-800 hover:bg-neutral-50 hover:border-emerald-300 transition-all duration-300 hover:scale-105 w-full md:w-auto"
            onClick={() => alert("macOS & Linux coming soon")}
          >
            <div className="flex items-center justify-center gap-3">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                  clipRule="evenodd"
                />
              </svg>
              <span>macOS / Linux (soon)</span>
            </div>
          </button>
        </div>

        <div className="mt-8 text-center text-xs text-neutral-500">
          <div className="inline-flex items-center gap-2 bg-white/50 px-4 py-2 rounded-full">
            <svg
              className="w-4 h-4 text-emerald-500"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
            Lightweight agent • No performance impact • Enterprise-ready
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
}
