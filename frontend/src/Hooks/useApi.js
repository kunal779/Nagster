// src/hooks/useApi.js
import { useState, useCallback } from "react";

const BACKEND_URL = "https://nagster.onrender.com";

export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const callApi = useCallback(async (endpoint, options = {}) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${BACKEND_URL}${endpoint}`, {
        headers: {
          "Content-Type": "application/json",
          ...(options.headers || {}),
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (err) {
      setError(err.message || "An unexpected error occurred");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { callApi, loading, error, setError };
}
