// src/hooks/useAuth.js
import { useState, useEffect } from "react";

// Custom hook to manage auth state
export function useAuth() {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedToken = sessionStorage.getItem("token");
    const storedUser = sessionStorage.getItem("user");

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const logout = () => {
    // Clear the sessionStorage and reset state
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("user");
    setToken(null);
    setUser(null);
  };

  return { token, user, setToken, setUser, logout }; // Return logout function
}
