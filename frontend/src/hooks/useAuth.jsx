// src/hooks/useAuth.jsx
import React, { createContext, useContext, useState, useEffect } from "react";
import { login as apiLogin, getCurrentUser } from "../api/auth";
import { setAuthToken } from "../api/client";
const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => sessionStorage.getItem("token"));
  const [user,  setUser ] = useState(() => {
    const raw = sessionStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  });

  useEffect(() => {
    if (!token) return;
    setAuthToken(token);
    getCurrentUser()
      .then(u => {
        setUser(u);
        sessionStorage.setItem("user", JSON.stringify(u));
      })
      .catch(() => {
        logout();
      });
  }, [token]);

  const login = async (email, password) => {
    const { access_token, user: u } = await apiLogin(email, password);
    sessionStorage.setItem("token", access_token);
    sessionStorage.setItem("user", JSON.stringify(u));
    setToken(access_token);
    setUser(u);
  };

  const logout = () => {
    setAuthToken(null);
    sessionStorage.clear();
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
