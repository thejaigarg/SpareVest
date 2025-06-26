// src/App.jsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/login";
import Signup from "./pages/signup";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/profile"; // Import Profile page
import Navbar from "./components/Navbar"; // (optional, create later)
import PrivateRoute from "./components/PrivateRoute"; // Import PrivateRoute component

export default function App() {
  return (
    <>
      {/* Show Navbar on all pages except login and signup */}
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Private routes */}
        <PrivateRoute path="/dashboard" element={<Dashboard />} />
        <PrivateRoute path="/profile" element={<Profile />} /> 

        {/* Add more routes as you build more pages */}
        <Route path="*" element={<div>404 Not Found</div>} />
      </Routes>
    </>
  );
}
