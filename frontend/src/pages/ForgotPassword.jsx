import React, { useState } from "react";
import { requestPasswordReset } from "../api/auth";
import { TextField, Button, Box, Typography, Alert, CircularProgress, Link } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

export default function ForgotPassword(){
    const [email, setEmail]= useState("");
    const [sent, setSent]= useState(false);
    const [error, setError]=useState("");
    const [loading, setLoading]=useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError("");
        setLoading(true);

        try {
            await requestPasswordReset(email);
            setSent(true);
        } catch (err) {
            const msg = err.response?.data?.detail || "Failed to send rest email";
            setError(msg);
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
            <Typography variant="h5" mb={2}>
                Forgot Password
            </Typography>
            {sent ? (
                <>
                    <Alert severity="success" sx={{ mb: 2 }}>
                    If an account with that email exists, you will receive a password reset link shortly.
                    </Alert>
                    <Button
                    component={RouterLink}
                    to="/login"
                    variant="outlined"
                    color="primary"
                    fullWidth
                    sx={{ mt: 2 }}
                    >
                    Back to Login
                    </Button>
                </>
            ) : (
                <form onSubmit={handleSubmit}>
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                <TextField
                    label="Email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    type="email"
                    fullWidth
                    margin="normal"
                    required
                />
                <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth
                    sx={{ mt: 2 }}
                    disabled={loading}
                >
                    {loading ? <CircularProgress size={24} /> : "Send Reset Link"}
                </Button>
                <Typography variant="body2" align="center" mt={2}>
                    <Link component={RouterLink} to="/login">
                        Back to Login
                    </Link>
                </Typography>
                </form>
            )}
        </Box>
    );
}