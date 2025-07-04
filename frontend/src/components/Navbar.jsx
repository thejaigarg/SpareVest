import React, { useState } from "react";
import { AppBar, Toolbar, Typography, Button, IconButton, Avatar, Menu, MenuItem, Box } from "@mui/material";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import { useAuth } from "../hooks/useAuth";
import { useNavigate, Link as RouterLink } from "react-router-dom";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  //For Avataar Menu
  const [ anchorEl, setAnchorEl ]=useState(null);
  const open = Boolean(anchorEl);

  if (!user) return null; // Don't render Navbar if not logged in

  const nameParts = user.full_name ? user.full_name.trim().split(" ") : [];
  const initials = nameParts.length >= 2
    ? (nameParts[0][0] + nameParts[1][0]).toUpperCase()
    : nameParts[0]?.[0]?.toUpperCase() || "?";

    const avatarUrl =
    user.avatarUrl ||
    `https://ui-avatars.com/api/?name=${encodeURIComponent(
      user.full_name || "User"
    )}&background=6366f1&color=fff`;

  //to open avatar menu  
  const handleAvatarClick = event => setAnchorEl(event.currentTarget);
  //to close menu
  const handleMenuClose = () => setAnchorEl(null);

  const handleProfile = () => {
    navigate("/profile");
    handleMenuClose();
  }  

  const handleLogout = () => {
    logout();
    navigate("/login");
    handleMenuClose();
  };

  return (
    <AppBar position="static" color="transparent" elevation={0}>
      <Toolbar>
        {/* Logo text at the left */}
        <Typography
          variant="h6"
          sx={{ flexGrow: 1, fontWeight: 700 }}
          component={RouterLink}
          to="/dashboard"
          style={{ color: "#222", textDecoration: "none" }}
        >
          SpareVest
        </Typography>

        {/* Notification bell icon */}
        <IconButton size="large" color="default">
          <NotificationsNoneIcon />
        </IconButton>

        {/* Avatar with menu */}
        <Box sx={{ ml: 1 }}>
          <IconButton onClick={handleAvatarClick} size="small">
            <Avatar src={avatarUrl} alt="User">
              {initials}
            </Avatar>
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={open}
            onClose={handleMenuClose}
            anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
            transformOrigin={{ vertical: "top", horizontal: "right" }}
          >
            <MenuItem onClick={handleProfile}>Profile</MenuItem>
            <MenuItem onClick={handleLogout}>Logout</MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
}