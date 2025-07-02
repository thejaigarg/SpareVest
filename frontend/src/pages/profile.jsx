// src/pages/Profile.jsx
import React, { useState } from "react";
import { Container, Typography, Button, Alert, Box } from "@mui/material";
import { requestPasswordReset } from "../api/auth";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

export default function Profile() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [message, setMessage] = useState("");
  const [error, setError]     = useState("");

  if (!user) return null;

  const handlePasswordReset = async () => {
    setMessage("");
    setError("");
    try {
      await requestPasswordReset(user.email);
      setMessage("If your email exists, a reset link has been sent.");
    } catch {
      setError("Error sending reset email.");
    }
  };

  return (
    <Box py={6}>
      <Container maxWidth="sm">
        <Typography variant="h5" gutterBottom>
          Profile
        </Typography>
        <Typography>Email: {user.email}</Typography>
        <Typography>Name: {user.full_name}</Typography>

        <Box mt={4} display="flex" gap={2}>
          <Button variant="outlined" onClick={handlePasswordReset}>
            Request Password Reset
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate("/profile/bank-account")}
          >
            Manage Bank Accounts
          </Button>
        </Box>

        {message && (
          <Alert severity="success" sx={{ mt: 2 }}>
            {message}
          </Alert>
        )}
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Container>
    </Box>
  );
}
