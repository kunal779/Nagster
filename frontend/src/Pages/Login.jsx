// src/Pages/Auth/Login.jsx
import React, { useCallback, useState } from "react";
import { Link } from "react-router-dom";
import { useApi } from "../Hooks/useApi";
import LoadingSpinner from "../Components/LoadingSpinner";
import logo from "../assets/logo.svg";

export default function Login({ onLogin }) {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [isHovered, setIsHovered] = useState(false);

  const { callApi, loading, error, setError } = useApi();

  const handleChange = useCallback(
    (field) => (e) => {
      setFormData((prev) => ({ ...prev, [field]: e.target.value }));
      if (error) setError(null);
    },
    [error, setError]
  );

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.username.trim() || !formData.password.trim()) {
      setError("Please fill in all fields");
      return;
    }

    try {
      const endpoint = "/auth/login";
      const body = {
        username: formData.username,
        password: formData.password,
      };

      const data = await callApi(endpoint, {
        method: "POST",
        body: JSON.stringify(body),
      });

      if (data?.access_token) {
        onLogin(data.access_token, data.role);
      } else {
        throw new Error(data?.detail || "Authentication failed");
      }
    } catch (err) {
      console.error("Login error:", err);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-gradient-to-br from-emerald-50 via-teal-50 to-sky-50 px-4">
      {/* Enhanced Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Animated gradient orbs */}
        <div className="absolute -top-40 -left-40 h-96 w-96 login-float-slow rounded-full bg-gradient-to-r from-emerald-200/40 to-teal-200/40 blur-3xl"></div>
        <div className="absolute -bottom-40 -right-40 h-96 w-96 login-float-slower rounded-full bg-gradient-to-r from-sky-200/40 to-emerald-200/40 blur-3xl"></div>
        <div className="absolute top-1/4 right-1/4 h-64 w-64 login-float-medium rounded-full bg-gradient-to-r from-teal-100/30 to-emerald-100/30 blur-3xl"></div>
        
        {/* Animated geometric shapes */}
        <div className="absolute top-20 left-10 h-32 w-32 login-spin-slow rounded-full border-[6px] border-emerald-200/20"></div>
        <div className="absolute bottom-32 right-20 h-24 w-24 login-spin-slower rounded-full border-[4px] border-teal-200/20"></div>
        
        {/* Floating lines */}
        <div className="absolute top-1/3 left-1/4 h-0.5 w-24 login-slide-right bg-gradient-to-r from-transparent via-emerald-300/20 to-transparent"></div>
        <div className="absolute bottom-1/3 right-1/4 h-0.5 w-24 login-slide-left bg-gradient-to-r from-transparent via-teal-300/20 to-transparent"></div>

        {/* Subtle dot grid */}
        <div 
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, #10b981 1px, transparent 0)`,
            backgroundSize: '40px 40px',
          }}
        />
        
        {/* Floating particles */}
        {[...Array(15)].map((_, i) => (
          <div
            key={i}
            className="absolute h-[2px] w-[2px] rounded-full bg-emerald-400/30"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animation: `login-float-particle 12s ease-in-out ${i * 0.3}s infinite`,
              animationDelay: `${i * 0.5}s`,
            }}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 w-full max-w-md">
        {/* Logo with enhanced design */}
        <div className="mb-8 flex flex-col items-center">
          <div className="relative mb-4">
            <div className="absolute inset-0 login-ping-slow rounded-full bg-emerald-200/30 blur-md"></div>
            <img 
              src={logo} 
              alt="Nagster logo" 
              className="relative h-20 w-20 object-contain drop-shadow-xl"
            />
          </div>
          <div className="text-center">
            <div className="mb-1 text-xs font-semibold tracking-widest text-emerald-600 uppercase">
              Nagster Admin
            </div>
            <div className="text-xs text-neutral-500">
              Secure Management Dashboard
            </div>
          </div>
        </div>

        {/* Login Card */}
        <div className="relative overflow-hidden rounded-3xl border border-emerald-100/60 bg-white/90 backdrop-blur-xl p-10 shadow-2xl shadow-emerald-200/20">
          {/* Card decoration */}
          <div className="absolute -top-20 -right-20 h-40 w-40 rounded-full bg-gradient-to-br from-emerald-100/10 to-teal-100/10 blur-xl"></div>
          <div className="absolute -bottom-20 -left-20 h-40 w-40 rounded-full bg-gradient-to-br from-sky-100/10 to-emerald-100/10 blur-xl"></div>
          
          <div className="relative">
            {/* Header */}
            <div className="mb-8 text-center">
              <h1 className="mb-3 text-2xl font-bold text-neutral-900">
                Welcome Back
                <span className="block h-1 w-16 mx-auto mt-2 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500"></span>
              </h1>
              <p className="text-sm text-neutral-600">
                Sign in to your Nagster dashboard
              </p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mb-6 login-shake flex items-center gap-3 rounded-xl border border-red-200 bg-red-50/80 px-4 py-3 text-sm text-red-600 backdrop-blur-sm">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-red-100">
                  <span className="text-red-600">!</span>
                </div>
                <span>{error}</span>
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Username Field */}
              <div className="group">
                <label className="mb-2 block text-sm font-semibold text-neutral-700">
                  Username
                </label>
                <div className="relative">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 group-focus-within:text-emerald-500">
                    👤
                  </div>
                  <input
                    value={formData.username}
                    onChange={handleChange("username")}
                    placeholder="Enter your username"
                    required
                    disabled={loading}
                    className="w-full rounded-xl border border-neutral-200 bg-white/90 pl-12 pr-4 py-3.5 text-sm text-neutral-900 outline-none transition-all duration-300 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-100 hover:border-emerald-300 disabled:cursor-not-allowed disabled:bg-neutral-50"
                  />
                </div>
              </div>

              {/* Password Field */}
              <div className="group">
                <label className="mb-2 block text-sm font-semibold text-neutral-700">
                  Password
                </label>
                <div className="relative">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400 group-focus-within:text-emerald-500">
                    🔒
                  </div>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={handleChange("password")}
                    placeholder="Enter your password"
                    required
                    disabled={loading}
                    className="w-full rounded-xl border border-neutral-200 bg-white/90 pl-12 pr-4 py-3.5 text-sm text-neutral-900 outline-none transition-all duration-300 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-100 hover:border-emerald-300 disabled:cursor-not-allowed disabled:bg-neutral-50"
                  />
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                className="group relative mt-2 inline-flex w-full items-center justify-center gap-3 overflow-hidden rounded-xl bg-gradient-to-r from-emerald-600 to-emerald-800 px-4 py-4 text-sm font-semibold text-white shadow-xl shadow-emerald-200/50 transition-all duration-500 hover:from-emerald-700 hover:to-emerald-900 hover:shadow-2xl hover:shadow-emerald-300/50 hover:-translate-y-1 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-70"
              >
                {/* Animated background effect */}
                <div className={`absolute inset-0 bg-gradient-to-r from-emerald-500 to-teal-500 transition-transform duration-500 ${isHovered ? 'translate-x-0' : '-translate-x-full'}`}></div>
                <div className="relative flex items-center gap-2">
                  {loading ? (
                    <>
                      <LoadingSpinner size={18} color="white" />
                      <span>Signing in...</span>
                    </>
                  ) : (
                    <>
                      <span className="text-lg">→</span>
                      <span>Sign In</span>
                    </>
                  )}
                </div>
              </button>
            </form>

            {/* Signup Link */}
            <div className="mt-8 text-center">
              <Link
                to="/signup"
                className="group inline-flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium text-emerald-600 transition-all duration-300 hover:bg-emerald-50"
              >
                <span className="group-hover:translate-x-1 transition-transform">
                  Don't have an account?
                </span>
                <span className="font-semibold group-hover:text-emerald-700">
                  Sign up
                </span>
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </Link>
            </div>

            {/* Divider */}
            <div className="relative my-8">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-neutral-200/50"></div>
              </div>
              <div className="relative flex justify-center">
                <span className="bg-white/90 px-4 text-xs text-neutral-500">or</span>
              </div>
            </div>

            {/* Back to Home */}
            <div className="text-center">
              <a
                href="/"
                className="inline-flex items-center gap-2 text-sm text-neutral-500 transition-all duration-300 hover:text-emerald-600"
              >
                <span className="rounded-full border border-neutral-300 p-1 transition-colors group-hover:border-emerald-300">
                  ←
                </span>
                <span className="group-hover:underline">Back to Nagster Home</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
// frontend change test
