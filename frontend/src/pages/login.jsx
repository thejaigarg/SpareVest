// src/pages/login.jsx
import React, { useState } from "react";
import { useEffect } from "react";
import { TextField, Button, Box, Typography, Alert, CircularProgress } from "@mui/material";
import { login as loginApi } from "../api/auth";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom"; // <-- Import useNavigate

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const { login, token } = useAuth();
  const navigate = useNavigate(); // <-- Create navigate

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
      const data = await loginApi(email, password);
      login(data.access_token, data.user); // Pass both token and user
      setSuccess(true);
      navigate("/dashboard");
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    }
    setLoading(false);
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
      <Typography variant="h5" mb={2}>Login</Typography>
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
    </Box>
  );
}
