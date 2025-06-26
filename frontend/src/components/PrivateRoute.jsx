// PrivateRoute.js
import React from "react";
import { Navigate } from "react-router-dom";

const PrivateRoute = ({ children }) => {
  const user = sessionStorage.getItem("user");
  return user ? children : <Navigate to="/login" replace />;
};

export default PrivateRoute;