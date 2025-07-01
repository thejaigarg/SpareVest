import React, { useState } from "react";
import { TextField, Button, Box, Typography, Alert, CircularProgress } from "@mui/material";
import { signup as signupApi, login as loginApi } from "../api/auth";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  // Basic validation
  const validate = () => {
    if (!email) return "Email is required";
    if (!/\S+@\S+\.\S+/.test(email)) return "Invalid email";
    if (!password) return "Password is required";
    if (password.length < 6) return "Password must be at least 6 characters";
    return "";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }
    setLoading(true);
    try {
      await signupApi({ email, full_name: fullName, password });
      const loginData = await loginApi(email, password);
      login(loginData.access_token, loginData.user); // Pass both token and user
      setSuccess(true);
      navigate("/dashboard");
    } catch (err) {
      setError(err?.response?.data?.detail || "Signup failed");
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
      <Typography variant="h5" mb={2}>Sign Up</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>Signup successful! Redirecting…</Alert>}
      <form onSubmit={handleSubmit}>
        <TextField
          label="Full Name"
          value={fullName}
          onChange={e => setFullName(e.target.value)}
          type="text"
          fullWidth
          margin="normal"
        />
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
          {loading ? <CircularProgress size={24} /> : "Sign Up"}
        </Button>
      </form>
      <Box mt={2} textAlign="center">
        <Typography variant="body2">
          Already have an account? <a href="/login">Login</a>
        </Typography>
      </Box>
    </Box>
  );
}
