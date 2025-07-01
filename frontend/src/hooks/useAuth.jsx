// src/hooks/useAuth.js
import React, { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  // Synchronously initialize from sessionStorage
  const [token, setToken] = useState(() => {
    return sessionStorage.getItem("token");
  });
  const [user, setUser] = useState(() => {
    const raw = sessionStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  });

  const login = (newToken, newUser) => {
    sessionStorage.setItem("token", newToken);
    sessionStorage.setItem("user", JSON.stringify(newUser));
    setToken(newToken);
    setUser(newUser);
  };

  const logout = () => {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("user");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
