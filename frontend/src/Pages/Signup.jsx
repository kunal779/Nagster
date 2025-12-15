// src/Pages/Auth/Signup.jsx
import React, { useCallback, useState } from "react";
import { Link } from "react-router-dom";
import { useApi } from "../Hooks/useApi";


import logo from "../assets/logo.svg";

export default function Signup({ onLogin }) {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    role: "admin",
  });

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
      const endpoint = "/auth/signup";
      const body = {
        username: formData.username,
        password: formData.password,
        role: formData.role,
      };

      const data = await callApi(endpoint, {
        method: "POST",
        body: JSON.stringify(body),
      });

      // Depending on backend, you might get token on signup or require login.
      // If backend returns access_token, log them in immediately.
      if (data?.access_token) {
        onLogin(data.access_token, data.role);
      } else {
        // if signup succeeded but no token, navigate user to login page
        // show a success message (simple alert for now)
        alert("Account created. Please sign in.");
      }
    } catch (err) {
      console.error("Signup error:", err);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-gradient-to-br from-emerald-50 via-teal-50 to-sky-50 px-4">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-24 -left-24 h-96 w-96 animate-pulse rounded-full bg-gradient-to-r from-emerald-100/30 to-teal-100/30 blur-3xl"></div>
        <div className="absolute -bottom-24 -right-24 h-96 w-96 animate-pulse rounded-full bg-gradient-to-r from-sky-100/30 to-emerald-100/30 blur-3xl animation-delay-2000"></div>

        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `linear-gradient(to right, #10b981 1px, transparent 1px),
                             linear-gradient(to bottom, #10b981 1px, transparent 1px)`,
            backgroundSize: "40px 40px",
          }}
        ></div>

        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute h-1 w-1 rounded-full bg-emerald-300/40"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animation: `float 8s ease-in-out ${i * 0.2}s infinite`,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 w-full max-w-md animate-fade-in">
        <div className="mb-10 flex justify-center">
          <img src={logo} alt="Nagster logo" className="h-16 w-16 object-contain drop-shadow-lg" />
        </div>

        <div className="rounded-3xl border border-emerald-100/50 bg-white/95 backdrop-blur-xl p-10 shadow-2xl shadow-emerald-200/30">
          <div className="mb-8 text-center">
            <h2 className="mb-2 text-3xl font-bold tracking-tight text-neutral-900 bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              Create Account
            </h2>
            <p className="text-sm text-neutral-600">Sign up for Nagster Admin Panel</p>
          </div>

          {error && (
            <div className="mb-5 animate-shake flex items-start gap-2 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
              <span className="text-base">⚠️</span>
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="grid gap-6">
            <div>
              <label className="mb-2 block text-sm font-semibold text-neutral-700">Username</label>
              <input
                value={formData.username}
                onChange={handleChange("username")}
                placeholder="Enter your username"
                required
                disabled={loading}
                className="w-full rounded-xl border border-neutral-200 bg-white/80 px-4 py-3.5 text-sm text-neutral-900 outline-none transition-all duration-300 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 focus:bg-white hover:border-emerald-300 disabled:cursor-not-allowed disabled:bg-neutral-50"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold text-neutral-700">Password</label>
              <input
                type="password"
                value={formData.password}
                onChange={handleChange("password")}
                placeholder="Create a password"
                required
                disabled={loading}
                className="w-full rounded-xl border border-neutral-200 bg-white/80 px-4 py-3.5 text-sm text-neutral-900 outline-none transition-all duration-300 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 focus:bg-white hover:border-emerald-300 disabled:cursor-not-allowed disabled:bg-neutral-50"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold text-neutral-700">Role</label>
              <select
                value={formData.role}
                onChange={handleChange("role")}
                disabled={loading}
                className="w-full rounded-xl border border-neutral-200 bg-white/80 px-4 py-3.5 text-sm text-neutral-900 outline-none transition-all duration-300 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 focus:bg-white hover:border-emerald-300 disabled:cursor-not-allowed disabled:bg-neutral-50"
              >
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-1 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-emerald-600 to-emerald-800 px-4 py-4 text-sm font-semibold text-white shadow-lg shadow-emerald-200 transition-all duration-300 hover:from-emerald-700 hover:to-emerald-900 hover:shadow-xl hover:shadow-emerald-300 hover:-translate-y-0.5 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {loading && <LoadingSpinner size={16} color="white" />}
              {loading ? "Please wait..." : "Create Account"}
            </button>
          </form>

          <div className="mt-8 text-center">
            <Link
              to="/admin"
              className="rounded-xl px-4 py-2 text-sm font-medium text-emerald-600 transition-all duration-300 hover:bg-emerald-50 hover:px-6"
            >
              Already have an account? Sign in
            </Link>
          </div>

          <div className="mt-8 pt-6 border-t border-neutral-200/50 text-center">
            <a href="/" className="inline-flex items-center gap-2 text-sm text-neutral-500 transition-all duration-300 hover:text-emerald-600 hover:gap-3">
              <span>←</span>
              <span>Back to Nagster Home</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
