// src/App.jsx
import React, { useEffect, useState, useCallback } from "react";
import Dashboard from "./Pages/Dashboard";
import { useApi } from "./Hooks/useApi";
import ErrorBoundary from "./Components/ErrorBoundary";
import LoadingSpinner from "./Components/LoadingSpinner";
import { COLORS, SHADOWS, primaryGradient } from "./Utils/colors";

function App() {
  const [token, setToken] = useState(() =>
    localStorage.getItem("nagster_token")
  );
  const [role, setRole] = useState(() => localStorage.getItem("nagster_role"));
  const [user, setUser] = useState(null);

  const { callApi: fetchUser } = useApi();

  const handleLogout = useCallback(() => {
    setToken(null);
    setRole(null);
    setUser(null);
    localStorage.removeItem("nagster_token");
    localStorage.removeItem("nagster_role");
  }, []);

  useEffect(() => {
    if (!token) return;

    const loadUser = async () => {
      try {
        const data = await fetchUser(
          `/auth/me?token=${encodeURIComponent(token)}`
        );
        if (data?.username) {
          setUser(data);
        } else {
          throw new Error("Invalid user data received");
        }
      } catch {
        handleLogout();
      }
    };

    loadUser();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const handleLogin = useCallback((newToken, newRole) => {
    setToken(newToken);
    setRole(newRole);
    localStorage.setItem("nagster_token", newToken);
    localStorage.setItem("nagster_role", newRole);
  }, []);

  // not logged in
  if (!token || !role) {
    return (
      <ErrorBoundary>
        <Login onLogin={handleLogin} />
      </ErrorBoundary>
    );
  }

  // logged in
  return (
    <ErrorBoundary>
      <Dashboard user={user} role={role} onLogout={handleLogout} />
    </ErrorBoundary>
  );
}

/* ========================= LOGIN COMPONENT ========================= */

function Login({ onLogin }) {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    role: "admin",
  });
  const [isSignup, setIsSignup] = useState(false);
  const { callApi, loading, error, setError } = useApi();

  const handleChange = useCallback(
    (field) => (e) => {
      setFormData((prev) => ({
        ...prev,
        [field]: e.target.value,
      }));
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
      const endpoint = isSignup ? "/auth/signup" : "/auth/login";
      const body = isSignup
        ? formData
        : {
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
      // error message hook me already set ho jayega
    }
  };

  const toggleMode = useCallback(() => {
    setIsSignup((prev) => !prev);
    setError(null);
  }, [setError]);

  return (
    <div
      style={{
        minHeight: "100vh",
        background: primaryGradient,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 16,
      }}
    >
      <div
        style={{
          background: "white",
          padding: "48px 40px",
          borderRadius: 24,
          width: "100%",
          maxWidth: 440,
          boxShadow: SHADOWS.xl,
          border: "1px solid rgba(255,255,255,0.2)",
        }}
      >
        {/* Logo + heading */}
        <div style={{ textAlign: "center", marginBottom: 32 }}>
          <div
            style={{
              width: 80,
              height: 80,
              background: primaryGradient,
              borderRadius: 20,
              margin: "0 auto 20px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "white",
              fontSize: 32,
              fontWeight: "bold",
              boxShadow: SHADOWS.lg,
            }}
          >
            N
          </div>
          <h2
            style={{
              marginBottom: 8,
              color: COLORS.gray[900],
              fontSize: 28,
              fontWeight: 700,
              letterSpacing: "-0.025em",
            }}
          >
            {isSignup ? "Create Account" : "Welcome Back"}
          </h2>
          <p
            style={{
              margin: 0,
              color: COLORS.gray[500],
              fontSize: 15,
              lineHeight: 1.5,
            }}
          >
            {isSignup
              ? "Sign up for Nagster"
              : "Sign in to your account to continue"}
          </p>
        </div>

        {/* Error message */}
        {error && (
          <div
            style={{
              background: COLORS.error[50],
              color: COLORS.error[600],
              padding: "12px 16px",
              borderRadius: 12,
              marginBottom: 24,
              fontSize: 14,
              border: `1px solid ${COLORS.error[200]}`,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span style={{ fontSize: 16 }}>⚠️</span>
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} style={{ display: "grid", gap: 20 }}>
          <div>
            <label
              style={{
                fontSize: 14,
                color: COLORS.gray[700],
                fontWeight: 600,
                display: "block",
                marginBottom: 8,
              }}
            >
              Username
            </label>
            <input
              value={formData.username}
              onChange={handleChange("username")}
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: 12,
                border: `1px solid ${COLORS.gray[300]}`,
                fontSize: 15,
                background: "#fff",
                color: COLORS.gray[900],
                transition: "all 0.2s ease",
                outline: "none",
              }}
              placeholder="Enter your username"
              required
              disabled={loading}
            />
          </div>

          <div>
            <label
              style={{
                fontSize: 14,
                color: COLORS.gray[700],
                fontWeight: 600,
                display: "block",
                marginBottom: 8,
              }}
            >
              Password
            </label>
            <input
              type="password"
              value={formData.password}
              onChange={handleChange("password")}
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: 12,
                border: `1px solid ${COLORS.gray[300]}`,
                fontSize: 15,
                background: "#fff",
                color: COLORS.gray[900],
                transition: "all 0.2s ease",
                outline: "none",
              }}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </div>

          {isSignup && (
            <div>
              <label
                style={{
                  fontSize: 14,
                  color: COLORS.gray[700],
                  fontWeight: 600,
                  display: "block",
                  marginBottom: 8,
                }}
              >
                Role
              </label>
              <select
                value={formData.role}
                onChange={handleChange("role")}
                style={{
                  width: "100%",
                  padding: "14px 16px",
                  borderRadius: 12,
                  border: `1px solid ${COLORS.gray[300]}`,
                  fontSize: 15,
                  background: "#fff",
                  color: COLORS.gray[900],
                  cursor: "pointer",
                  outline: "none",
                }}
                disabled={loading}
              >
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
              </select>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              marginTop: 8,
              padding: "16px",
              borderRadius: 12,
              border: "none",
              background: primaryGradient,
              color: "white",
              fontWeight: 600,
              fontSize: 15,
              cursor: loading ? "not-allowed" : "pointer",
              transition: "all 0.2s ease",
              opacity: loading ? 0.7 : 1,
              boxShadow: SHADOWS.md,
              width: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 8,
            }}
          >
            {loading && <LoadingSpinner size={16} color="white" />}
            {loading ? "Please wait..." : isSignup ? "Create Account" : "Sign In"}
          </button>
        </form>

        {/* Toggle login/signup */}
        <div style={{ textAlign: "center", marginTop: 24 }}>
          <button
            type="button"
            onClick={toggleMode}
            disabled={loading}
            style={{
              background: "none",
              border: "none",
              color: COLORS.primary[500],
              fontSize: 14,
              cursor: loading ? "not-allowed" : "pointer",
              fontWeight: 500,
              padding: "8px 12px",
              borderRadius: 8,
              opacity: loading ? 0.5 : 1,
            }}
          >
            {isSignup
              ? "Already have an account? Sign in"
              : "Don't have an account? Sign up"}
          </button>
        </div>
      </div>

      <style>{`
        input:focus, select:focus {
          border-color: ${COLORS.primary[500]} !important;
          box-shadow: 0 0 0 3px ${COLORS.primary[100]};
        }
        
        input:disabled, select:disabled {
          background-color: ${COLORS.gray[50]};
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
}

export default App;
