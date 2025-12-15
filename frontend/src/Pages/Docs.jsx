import React, { useState } from 'react';

import {
  FaBook,
  FaCode,
  FaServer,
  FaDesktop,
  FaShieldAlt,
  FaChartLine,
  FaCheckCircle,
  FaQuestionCircle,
  FaCogs,
  FaDatabase,
  FaLock,
  FaUsers,
  FaEye,
  FaClock,
  FaExclamationTriangle,
  FaTerminal,
  FaDownload,
  FaKey,
  FaGlobe,
  FaMobileAlt,
  FaSync
} from "react-icons/fa";


const Docs = () => {
  const [activeSection, setActiveSection] = useState('overview');

  const sections = [
    { id: 'overview', label: 'Overview', icon: <FaBook /> },
    { id: 'architecture', label: 'Architecture', icon: <FaChartLine /> },
    { id: 'agent', label: 'Agent Setup', icon: <FaDesktop /> },
    { id: 'security', label: 'Security', icon: <FaShieldAlt /> },
    { id: 'troubleshooting', label: 'FAQ', icon: <FaQuestionCircle /> }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#f7f5ef] to-neutral-50 text-gray-900">
      {/* Header */}
      <div className="bg-white border-b border-neutral-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-gray-900 flex items-center gap-3">
                <FaBook className="text-emerald-600" />
                Nagster Documentation
              </h1>
              <p className="text-gray-700 mt-2 text-sm md:text-base">
                Complete guide to setup, configure, and manage your Nagster monitoring system
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:w-1/4">
            <div className="sticky top-24 bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <FaBook className="text-emerald-600" />
                Documentation
              </h3>
              <nav className="space-y-2">
                {sections.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`w-full text-left px-4 py-3 rounded-xl flex items-center gap-3 transition-all duration-200 ${
                      activeSection === section.id
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    {section.icon}
                    <span className="font-medium text-sm md:text-base">{section.label}</span>
                  </button>
                ))}
              </nav>

              {/* Quick Links */}
              <div className="mt-8 pt-6 border-t border-gray-200">
                <h4 className="text-sm font-semibold text-gray-900 mb-3">Quick Links</h4>
                <div className="space-y-2">
                  <a href="#" className="text-sm text-emerald-600 hover:text-emerald-700 flex items-center gap-2">
                    <FaDownload /> Agent Download
                  </a>
                  <a href="#" className="text-sm text-emerald-600 hover:text-emerald-700 flex items-center gap-2">
                    <FaShieldAlt /> Security Guide
                  </a>
                  <a href="#" className="text-sm text-emerald-600 hover:text-emerald-700 flex items-center gap-2">
                    <FaQuestionCircle /> Support
                  </a>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:w-3/4">
            {/* OVERVIEW SECTION */}
            {activeSection === 'overview' && (
              <div className="space-y-8">
                <div className="bg-gradient-to-r from-emerald-50 to-white rounded-2xl p-6 md:p-8 shadow-lg border border-emerald-100">
                  <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6 flex items-center gap-3">
                    <FaBook className="text-emerald-600" />
                    Nagster System Overview
                  </h2>
                  
                  <div className="grid md:grid-cols-2 gap-6 md:gap-8 mb-8">
                    <div className="bg-white rounded-xl p-6 shadow-md border border-gray-200">
                      <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 md:w-12 md:h-12 rounded-lg bg-gradient-to-br from-emerald-600 to-emerald-800 flex items-center justify-center">
                          <FaDesktop className="text-white text-lg md:text-xl" />                        </div>
                        <h3 className="text-xl font-bold text-gray-900">Nagster Agent</h3>
                      </div>
                      <p className="text-gray-700 mb-4 text-sm md:text-base">
                        Lightweight desktop application that runs on employee systems to monitor activity patterns.
                      </p>
                      <ul className="space-y-2 md:space-y-3">
                        <li className="flex items-center gap-2 text-sm md:text-base">
                          <FaCheckCircle className="text-emerald-500 flex-shrink-0" />
                          <span>Runs on employee workstation</span>
                        </li>
                        <li className="flex items-center gap-2 text-sm md:text-base">
                          <FaCheckCircle className="text-emerald-500 flex-shrink-0" />
                          <span>Tracks keyboard, mouse & app activity</span>
                        </li>
                        <li className="flex items-center gap-2 text-sm md:text-base">
                          <FaCheckCircle className="text-emerald-500 flex-shrink-0" />
                          <span>Detects idle & suspicious patterns</span>
                        </li>
                        <li className="flex items-center gap-2 text-sm md:text-base">
                          <FaCheckCircle className="text-emerald-500 flex-shrink-0" />
                          <span>Can trigger auto lock/logout</span>
                        </li>
                      </ul>
                    </div>

                    <div className="bg-white rounded-xl p-6 shadow-md border border-gray-200">
                      <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 md:w-12 md:h-12 rounded-lg bg-gradient-to-br from-emerald-600 to-emerald-800 flex items-center justify-center">
                          <FaEye className="text-white text-lg md:text-xl" />
                        </div>
                        <h3 className="text-xl font-bold text-gray-900">Admin Panel</h3>
                      </div>
                      <p className="text-gray-700 mb-4 text-sm md:text-base">
                        Web-based dashboard for managers and HR to monitor team activity and productivity.
                      </p>
                      <ul className="space-y-2 md:space-y-3">
                        <li className="flex items-center gap-2 text-sm md:text-base">
                          <FaCheckCircle className="text-emerald-500 flex-shrink-0" />
                          <span>Accessible to managers/HR</span>
                        </li>
                        <li className="flex items-center gap-2 text-sm md:text-base">
                          <FaCheckCircle className="text-emerald-500 flex-shrink-0" />
                          <span>Real-time activity monitoring</span>
                        </li>
                        <li className="flex items-center gap-2 text-sm md:text-base">
                          <FaCheckCircle className="text-emerald-500 flex-shrink-0" />
                          <span>Detailed analytics & reports</span>
                        </li>
                        <li className="flex items-center gap-2 text-sm md:text-base">
                          <FaCheckCircle className="text-emerald-500 flex-shrink-0" />
                          <span>Policy configuration</span>
                        </li>
                      </ul>
                    </div>
                  </div>

                  <div className="bg-white rounded-xl p-6 shadow-md border border-emerald-200">
                    <h3 className="text-xl font-bold text-gray-900 mb-4">How It Works</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="text-center">
                        <div className="w-14 h-14 md:w-16 md:h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-3">
                          <FaDesktop className="text-emerald-600 text-xl md:text-2xl" />
                        </div>
                        <h4 className="font-semibold mb-2 text-sm md:text-base">Agent Collects Data</h4>
                        <p className="text-xs md:text-sm text-gray-700">Agent on employee system monitors activity</p>
                      </div>
                      <div className="text-center">
                        <div className="w-14 h-14 md:w-16 md:h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-3">
                          <FaSync className="text-emerald-600 text-xl md:text-2xl" />
                        </div>
                        <h4 className="font-semibold mb-2 text-sm md:text-base">Data Syncs Securely</h4>
                        <p className="text-xs md:text-sm text-gray-700">Encrypted data sent to backend</p>
                      </div>
                      <div className="text-center">
                        <div className="w-14 h-14 md:w-16 md:h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-3">
                          <FaEye className="text-emerald-600 text-xl md:text-2xl" />
                        </div>
                        <h4 className="font-semibold mb-2 text-sm md:text-base">Manager Views Dashboard</h4>
                        <p className="text-xs md:text-sm text-gray-700">Real-time insights on admin panel</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* ARCHITECTURE SECTION */}
            {activeSection === 'architecture' && (
              <div className="space-y-8">
                <div className="bg-white rounded-2xl p-6 md:p-8 shadow-lg border border-gray-200">
                  <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6 flex items-center gap-3">
                    <FaChartLine className="text-emerald-600" />
                    Architecture Overview
                  </h2>
                  
                  <div className="mb-8">
                    <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-4">Three Core Components</h3>
                    
                    <div className="grid md:grid-cols-3 gap-6 mb-8">
                      <div className="bg-gradient-to-b from-emerald-50 to-white p-6 rounded-xl border border-emerald-200">
                        <div className="flex items-center gap-3 mb-4">
                          <div className="w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center">
                            <FaDesktop className="text-white" />
                          </div>
                          <h4 className="text-lg font-bold text-gray-900">Agent</h4>
                        </div>
                        <p className="text-gray-700 mb-3 text-sm md:text-base">
                          Python application running on employee workstations.
                        </p>
                        <div className="text-xs md:text-sm text-gray-600 space-y-1">
                          <p>• Tracks keyboard/mouse events</p>
                          <p>• Detects idle & suspicious patterns</p>
                          <p>• Sends activity logs to backend</p>
                        </div>
                      </div>

                      <div className="bg-gradient-to-b from-emerald-50 to-white p-6 rounded-xl border border-emerald-200">
                        <div className="flex items-center gap-3 mb-4">
                          <div className="w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center">
                            <FaServer className="text-white" />
                          </div>
                          <h4 className="text-lg font-bold text-gray-900">Backend API</h4>
                        </div>
                        <p className="text-gray-700 mb-3 text-sm md:text-base">
                          FastAPI service handling data storage and processing.
                        </p>
                        <div className="text-xs md:text-sm text-gray-600 space-y-1">
                          <p>• Receives activity logs</p>
                          <p>• Stores data in database</p>
                          <p>• Provides APIs for dashboard</p>
                        </div>
                      </div>

                      <div className="bg-gradient-to-b from-emerald-50 to-white p-6 rounded-xl border border-emerald-200">
                        <div className="flex items-center gap-3 mb-4">
                          <div className="w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center">
                            <FaEye className="text-white" />
                          </div>
                          <h4 className="text-lg font-bold text-gray-900">Dashboard</h4>
                        </div>
                        <p className="text-gray-700 mb-3 text-sm md:text-base">
                          React-based admin interface for monitoring and management.
                        </p>
                        <div className="text-xs md:text-sm text-gray-600 space-y-1">
                          <p>• Real-time activity view</p>
                          <p>• Analytics & reports</p>
                          <p>• Configuration interface</p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-gradient-to-r from-slate-50 to-white p-6 rounded-xl border border-slate-200">
                      <h4 className="text-lg font-bold text-gray-900 mb-4">Data Flow</h4>
                      <div className="flex items-center justify-between mb-4 overflow-x-auto">
                        <div className="text-center min-w-[80px]">
                          <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-2">
                            <FaDesktopIcon className="text-emerald-600" />
                          </div>
                          <span className="text-sm font-medium">Agent</span>
                        </div>
                        <div className="flex-1 h-1 bg-emerald-200 mx-4 relative min-w-[40px]">
                          <div className="absolute inset-0 bg-gradient-to-r from-emerald-400 to-emerald-600 animate-pulse rounded-full"></div>
                        </div>
                        <div className="text-center min-w-[80px]">
                          <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-2">
                            <FaServer className="text-emerald-600" />
                          </div>
                          <span className="text-sm font-medium">Backend</span>
                        </div>
                        <div className="flex-1 h-1 bg-emerald-200 mx-4 relative min-w-[40px]">
                          <div className="absolute inset-0 bg-gradient-to-r from-emerald-400 to-emerald-600 animate-pulse rounded-full"></div>
                        </div>
                        <div className="text-center min-w-[80px]">
                          <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-2">
                            <FaEye className="text-emerald-600" />
                          </div>
                          <span className="text-sm font-medium">Dashboard</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* AGENT SETUP SECTION */}
            {activeSection === 'agent' && (
              <div className="space-y-8">
                <div className="bg-white rounded-2xl p-6 md:p-8 shadow-lg border border-gray-200">
                  <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6 flex items-center gap-3">
                    <FaDesktop className="text-emerald-600" />
                    Agent Setup Guide
                  </h2>
                  
                  <div className="space-y-6">
                    <div className="bg-gradient-to-r from-emerald-50 to-white p-6 rounded-xl border border-emerald-200">
                      <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                        <FaDownload className="text-emerald-600" />
                        Installation
                      </h3>
                      <div className="space-y-4">
                        <div className="bg-white p-4 rounded-lg border border-gray-200">
                          <h4 className="font-semibold text-gray-900 mb-2">Step 1: Download Agent</h4>
                          <div className="flex items-center gap-4 mt-3 flex-wrap">
                            <button
                              onClick={() => {
                                const link = document.createElement('a');
                                link.href = '/agent.exe';
                                link.download = 'Nagster-Agent-Setup.exe';
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                              }}
                              className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
                            >
                              <FaDownload />
                              Windows Agent
                            </button>
                            <span className="text-sm text-gray-600">macOS & Linux coming soon</span>
                          </div>
                        </div>

                        <div className="bg-white p-4 rounded-lg border border-gray-200">
                          <h4 className="font-semibold text-gray-900 mb-2">Step 2: Run Installer</h4>
                          <p className="text-gray-700 mb-2 text-sm md:text-base">Double-click the installer and Enter Employee Unique ID.</p>
                          <div className="text-xs md:text-sm text-gray-600 bg-gray-50 p-3 rounded mt-2">
                            <p>✓ Installs as system service (Windows)</p>
                            <p>✓ Auto-starts with system boot</p>
                            <p>✓ Runs in background</p>
                          </div>
                        </div>

                        <div className="bg-white p-4 rounded-lg border border-gray-200">
                          <h4 className="font-semibold text-gray-900 mb-2">Step 3: Configuration</h4>
                          <p className="text-gray-700 mb-3 text-sm md:text-base">Agent will ask for:</p>
                          <div className="grid md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                              <div className="flex items-center gap-2">
                                <FaKey className="text-emerald-500 text-sm" />
                                <span className="font-medium">Employee ID</span>
                              </div>
                              <p className="text-sm text-gray-700">Provided by your organization</p>
                            </div>
                            <div className="space-y-2">
                              <div className="flex items-center gap-2">
                                <FaServer className="text-emerald-500 text-sm" />
                                <span className="font-medium">Backend URL</span>
                              </div>
                              <p className="text-sm text-gray-700">Auto-filled by admin</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-gradient-to-r from-blue-50 to-white p-6 rounded-xl border border-blue-200 overflow-x-auto">
                      <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                        <FaCogs className="text-blue-600" />
                        Configuration Options
                      </h3>
                      <table className="w-full border-collapse min-w-[600px]">
                        <thead>
                          <tr className="bg-gray-50">
                            <th className="text-left p-3 border border-gray-200 text-sm md:text-base">Setting</th>
                            <th className="text-left p-3 border border-gray-200 text-sm md:text-base">Description</th>
                            <th className="text-left p-3 border border-gray-200 text-sm md:text-base">Default</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td className="p-3 border border-gray-200 font-medium text-sm md:text-base">Idle Threshold</td>
                            <td className="p-3 border border-gray-200 text-sm md:text-base">Time before marking as idle</td>
                            <td className="p-3 border border-gray-200 text-emerald-600 text-sm md:text-base">300 seconds</td>
                          </tr>
                          <tr>
                            <td className="p-3 border border-gray-200 font-medium text-sm md:text-base">Auto Lock</td>
                            <td className="p-3 border border-gray-200 text-sm md:text-base">Action after idle timeout</td>
                            <td className="p-3 border border-gray-200 text-emerald-600 text-sm md:text-base">Lock workstation</td>
                          </tr>
                          <tr>
                            <td className="p-3 border border-gray-200 font-medium text-sm md:text-base">Suspicious Threshold</td>
                            <td className="p-3 border border-gray-200 text-sm md:text-base">Key repeats for fake activity</td>
                            <td className="p-3 border border-gray-200 text-emerald-600 text-sm md:text-base">50 keys</td>
                          </tr>
                          <tr>
                            <td className="p-3 border border-gray-200 font-medium text-sm md:text-base">Sync Interval</td>
                            <td className="p-3 border border-gray-200 text-sm md:text-base">Data send frequency</td>
                            <td className="p-3 border border-gray-200 text-emerald-600 text-sm md:text-base">60 seconds</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* SECURITY SECTION */}
            {activeSection === 'security' && (
              <div className="space-y-8">
                <div className="bg-white rounded-2xl p-6 md:p-8 shadow-lg border border-gray-200">
                  <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6 flex items-center gap-3">
                    <FaShieldAlt className="text-emerald-600" />
                    Security & Privacy
                  </h2>
                  
                  <div className="space-y-6">
                    <div className="bg-gradient-to-r from-emerald-50 to-white p-6 rounded-xl border border-emerald-200">
                      <h3 className="text-xl font-bold text-gray-900 mb-4">Privacy First Design</h3>
                      <div className="grid md:grid-cols-2 gap-6">
                        <div className="space-y-3">
                          <div className="flex items-center gap-3">
                            <FaLock className="text-emerald-600" />
                            <h4 className="font-semibold">What We Don't Track</h4>
                          </div>
                          <ul className="space-y-2 text-gray-700">
                            <li className="flex items-center gap-2 text-sm md:text-base">
                              <FaCheckCircle className="text-emerald-500 text-sm flex-shrink-0" />
                              No keystroke content logging
                            </li>
                            <li className="flex items-center gap-2 text-sm md:text-base">
                              <FaCheckCircle className="text-emerald-500 text-sm flex-shrink-0" />
                              No screenshot capturing
                            </li>
                            <li className="flex items-center gap-2 text-sm md:text-base">
                              <FaCheckCircle className="text-emerald-500 text-sm flex-shrink-0" />
                              No clipboard monitoring
                            </li>
                            <li className="flex items-center gap-2 text-sm md:text-base">
                              <FaCheckCircle className="text-emerald-500 text-sm flex-shrink-0" />
                              No personal file access
                            </li>
                          </ul>
                        </div>
                        <div className="space-y-3">
                          <div className="flex items-center gap-3">
                            <FaEye className="text-emerald-600" />
                            <h4 className="font-semibold">What We Track</h4>
                          </div>
                          <ul className="space-y-2 text-gray-700">
                            <li className="flex items-center gap-2 text-sm md:text-base">
                              <FaCheckCircle className="text-emerald-500 text-sm flex-shrink-0" />
                              Activity timing patterns
                            </li>
                            <li className="flex items-center gap-2 text-sm md:text-base">
                              <FaCheckCircle className="text-emerald-500 text-sm flex-shrink-0" />
                              Application names (not content)
                            </li>
                            <li className="flex items-center gap-2 text-sm md:text-base">
                              <FaCheckCircle className="text-emerald-500 text-sm flex-shrink-0" />
                              Active/idle status
                            </li>
                            <li className="flex items-center gap-2 text-sm md:text-base">
                              <FaCheckCircle className="text-emerald-500 text-sm flex-shrink-0" />
                              Suspicious pattern flags
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>

                    <div className="bg-gradient-to-r from-blue-50 to-white p-6 rounded-xl border border-blue-200">
                      <h3 className="text-xl font-bold text-gray-900 mb-4">Security Features</h3>
                      <div className="grid md:grid-cols-3 gap-6">
                        <div className="text-center p-4 bg-white rounded-lg border border-blue-100">
                          <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-3">
                            <FaLock className="text-blue-600 text-lg md:text-xl" />
                          </div>
                          <h4 className="font-semibold mb-2 text-sm md:text-base">Data Encryption</h4>
                          <p className="text-xs md:text-sm text-gray-700">All data encrypted in transit and at rest</p>
                        </div>
                        <div className="text-center p-4 bg-white rounded-lg border border-blue-100">
                          <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-3">
                            <FaUsers className="text-blue-600 text-lg md:text-xl" />
                          </div>
                          <h4 className="font-semibold mb-2 text-sm md:text-base">Role-Based Access</h4>
                          <p className="text-xs md:text-sm text-gray-700">Strict permission levels for admins</p>
                        </div>
                        <div className="text-center p-4 bg-white rounded-lg border border-blue-100">
                          <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-3">
                            <FaDatabase className="text-blue-600 text-lg md:text-xl" />
                          </div>
                          <h4 className="font-semibold mb-2 text-sm md:text-base">Compliance Ready</h4>
                          <p className="text-xs md:text-sm text-gray-700">SOC 2, GDPR, and industry standards</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* FAQ SECTION */}
            {activeSection === 'troubleshooting' && (
              <div className="space-y-8">
                <div className="bg-white rounded-2xl p-6 md:p-8 shadow-lg border border-gray-200">
                  <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6 flex items-center gap-3">
                    <FaQuestionCircle className="text-emerald-600" />
                    Frequently Asked Questions
                  </h2>
                  
                  <div className="space-y-4">
                    {[
                      {
                        q: "How does Nagster protect employee privacy?",
                        a: "Nagster only tracks activity metadata (timing, app names) and never records content. We don't capture keystrokes, screenshots, or personal data."
                      },
                      {
                        q: "Can employees disable the agent?",
                        a: "No, the agent is designed to run continuously with proper permissions. This ensures accurate monitoring and compliance with company policies."
                      },
                      {
                        q: "What happens when internet is disconnected?",
                        a: "Agent stores data locally and syncs when connection is restored. Critical features like auto-lock work offline."
                      },
                      {
                        q: "How are false positives handled?",
                        a: "Our smart algorithms differentiate between real work and suspicious patterns. Thresholds are configurable to match your team's workflow."
                      },
                      {
                        q: "Is Nagster compatible with remote desktop/VPN?",
                        a: "Yes, Nagster works seamlessly with RDP, VPN, and all standard remote work setups."
                      }
                    ].map((faq, index) => (
                      <div key={index} className="bg-gradient-to-r from-emerald-50 to-white p-6 rounded-xl border border-emerald-200">
                        <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
                          <FaQuestionCircle className="text-emerald-600" />
                          {faq.q}
                        </h3>
                        <p className="text-gray-700 pl-8 text-sm md:text-base">{faq.a}</p>
                      </div>
                    ))}
                  </div>

                  <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-white rounded-xl border border-blue-200">
                    <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                      <FaExclamationTriangle className="text-blue-600" />
                      Need More Help?
                    </h3>
                    <p className="text-gray-700 mb-4 text-sm md:text-base">
                      Can't find what you're looking for? Our support team is here to help.
                    </p>
                    <div className="flex items-center gap-4 flex-wrap">
                      <button className="inline-flex items-center gap-2 px-4 py-2 md:px-6 md:py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm md:text-base">
                        <FaQuestionCircle />
                        Contact Support
                      </button>
                      <button className="text-blue-600 hover:text-blue-700 text-sm md:text-base">
                        View complete troubleshooting guide →
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Docs;