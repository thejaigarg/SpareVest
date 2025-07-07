// src/pages/login.jsx
import React, { useState, useEffect } from "react";
import { TextField, Button, Box, Typography, Alert, CircularProgress } from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const { login, token } = useAuth();
  const navigate = useNavigate();

  // If already authenticated, go straight to dashboard
  useEffect(() => {
    if (token) {
      navigate("/dashboard");
    }
  }, [token, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);

    try {
      // CALL YOUR CONTEXT LOGIN ONLY
      await login(email, password);
      setSuccess(true);
      navigate("/dashboard");
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      maxWidth={400}
      mx="auto"
      mt={8}
      p={4}
      display="flex"
      flexDirection="column"
      boxShadow={3}
      borderRadius={2}
      bgcolor="background.paper"
    >

      <Box display="flex" justifyContent="center" mb={2}>
        <img
          src="/logo.png"
          alt="SpareVest Logo"
          style={{ maxWidth: 300, height: "auto" }}
        />
      </Box>
       
      <Box display="flex" justifyContent="center" mb={1}>
        <Typography
  variant="h4"
  fontWeight="bold"
  letterSpacing={0}
  sx={{
    background: "linear-gradient(90deg, #06b6d4 0%,rgb(6, 183, 124) 100%)", // cyan to sea green
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
    textFillColor: "transparent",
    textShadow: "0 2px 8px rgba(0,0,0,0.08)",
    fontFamily: "Montserrat, Roboto, Arial, sans-serif",
    fontWeight: 900,
    fontSize: { xs: "2.2rem", md: "2.8rem" },
  }}
>
  SpareVest
</Typography>

      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>Login successful!</Alert>}
      <form onSubmit={handleSubmit}>
        <TextField
          label="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          type="email"
          fullWidth
          margin="normal"
          required
        />
        <TextField
          label="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          type="password"
          fullWidth
          margin="normal"
          required
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          disabled={loading}
          sx={{ mt: 2 }}
        >
          {loading ? <CircularProgress size={24} /> : "Login"}
        </Button>
      </form>
      <Box mt={2} textAlign="center">
        <Typography variant="body2">
          Don&apos;t have an account? <a href="/signup">Sign up</a>
        </Typography>
      </Box>
      <Box mt={1} textAlign="center">
        <Typography variant="body2">
          <a href="/forgot-password">Forgot password?</a>
        </Typography>
      </Box>
    </Box>
  );
}
