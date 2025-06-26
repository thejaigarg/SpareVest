// src/pages/Profile.jsx
import React, { useState } from "react";
import { Container, Typography, Button, Alert, Box } from "@mui/material";
import { requestPasswordReset } from "../api/auth";
import { useAuth } from "../hooks/useAuth";

export default function Profile() {
  const { token, user, setUser } = useAuth(); // Use the token and user from useAuth hook
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handlePasswordReset = async () => {
    setMessage("");
    setError("");
    try {
      await requestPasswordReset(user.email);
      setMessage("If your email exists, a reset link has been sent.");
    } catch (err) {
      setError("Error sending reset email.");
    }
  };

  if (!user) return null; // Don't render the component if the user is not found

  return (
    <Box py={6}>
      <Container maxWidth="sm">
        <Typography variant="h5" gutterBottom>Profile</Typography>
        <Typography>Email: {user.email}</Typography>
        <Typography>Name: {user.full_name}</Typography>
        <Button variant="outlined" sx={{ mt: 2 }} onClick={handlePasswordReset}>
          Request Password Reset
        </Button>
        {message && <Alert severity="success" sx={{ mt: 2 }}>{message}</Alert>}
        {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      </Container>
    </Box>
  );
}
