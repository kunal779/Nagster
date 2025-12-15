// src/App.jsx
import React, { useEffect, useState, useCallback } from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import Dashboard from "./Pages/Dashboard";
import Home from "./Pages/Home";
import { useApi } from "./Hooks/useApi";
import ErrorBoundary from "./Components/ErrorBoundary";
import Docs from "./Pages/Docs";

import Login from "./Pages/Login";
import Signup from "./Pages/Signup";

function App() {
  const [token, setToken] = useState(() =>
    localStorage.getItem("nagster_token")
  );
  const [role, setRole] = useState(() => localStorage.getItem("nagster_role"));
  const [user, setUser] = useState(null);

  const { callApi: fetchUser } = useApi();
  const navigate = useNavigate();

  const handleLogout = useCallback(() => {
    setToken(null);
    setRole(null);
    setUser(null);
    localStorage.removeItem("nagster_token");
    localStorage.removeItem("nagster_role");
    navigate("/admin");
  }, [navigate]);

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
  }, [token, fetchUser, handleLogout]);

  const handleLogin = useCallback(
    (newToken, newRole) => {
      setToken(newToken);
      setRole(newRole);
      localStorage.setItem("nagster_token", newToken);
      localStorage.setItem("nagster_role", newRole);
      navigate("/dashboard");
    },
    [navigate]
  );

  return (
    <ErrorBoundary>
      <Routes>
        {/* Landing / marketing home */}
        <Route path="/" element={<Home />} />

        {/* Admin login */}
        <Route path="/admin" element={<Login onLogin={handleLogin} />} />

        {/* Signup page */}
        <Route path="/signup" element={<Signup onLogin={handleLogin} />} />

        {/* Docs page */}
        <Route path="/docs" element={<Docs />} />

        {/* Protected dashboard */}
        <Route
          path="/dashboard"
          element={
            token && role ? (
              <Dashboard user={user} role={role} onLogout={handleLogout} />
            ) : (
              <Navigate to="/admin" replace />
            )
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </ErrorBoundary>
  );
}

export default App;
