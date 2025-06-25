import { useState } from "react";

// Util to get token from storage (so it works on refresh)
function getInitialToken() {
  return localStorage.getItem("token");
}

export function useAuth() {
  const [token, setToken] = useState(getInitialToken());

  // Call this on successful login
  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  // Call this to logout user
  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  // Returns true if logged in
  const isAuthenticated = !!token;

  // You can expand this later (e.g., decode JWT for user info)

  return { token, login, logout, isAuthenticated };
}
