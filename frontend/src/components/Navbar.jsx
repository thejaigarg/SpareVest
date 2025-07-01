import React from "react";
import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import { useNavigate, Link } from "react-router-dom";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  if (!user) return null; // Don't render Navbar if not logged in

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
        <Button color="inherit" component={Link} to="/profile">
          {user.full_name || user.email}
        </Button>
        <Button color="inherit" onClick={handleLogout}>Logout</Button>
      </Toolbar>
    </AppBar>
  );
}