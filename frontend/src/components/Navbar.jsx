// src/components/Navbar.jsx
import React, { useEffect, useState } from "react";
import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import { useNavigate, Link } from "react-router-dom";
import { getCurrentUser } from "../api/auth";

export default function Navbar() {
  const { token, logout } = useAuth();
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      getCurrentUser(token)
        .then(setUser)
        .catch(() => setUser(null));
    }
  }, [token]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          <Link to="/dashboard" style={{ color: "#fff", textDecoration: "none" }}>SpareVest</Link>
        </Typography>
        {user && (
          <>
            <Button color="inherit" component={Link} to="/profile">
              {user.full_name || user.email}
            </Button>
            <Button color="inherit" onClick={handleLogout}>Logout</Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}
