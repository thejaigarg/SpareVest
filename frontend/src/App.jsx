// src/App.jsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/login";
//import Signup from "./pages/signup";
import Dashboard from "./pages/dashboard";
//import Navbar from "./components/Navbar"; // (optional, create later)

export default function App() {
  return (
    <>
      {/* Optional: <Navbar /> */}
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        {/* <Route path="/signup" element={<Signup />} /> */}
        <Route path="/dashboard" element={<Dashboard />} />
        {/* Add more routes as you build more pages */}
        <Route path="*" element={<div>404 Not Found</div>} />
      </Routes>
    </>
  );
}
