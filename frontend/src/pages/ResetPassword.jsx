import React, { useState } from "react";
import { useSearchParams, Link as RouterLink } from "react-router-dom";
import { Box, Alert, Button, Typography, TextField, CircularProgress } from "@mui/material";
import { resetPassword } from "../api/auth";

export default function ResetPassword() {
    const [searchParams] = useSearchParams();
    const token = searchParams.get("token");

    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        if (!password || !confirmPassword) {
            setError("Please enter and confirm your new password");
            return;
        }
        if (password !== confirmPassword) {
            setError("Passwords do not match!");
            return;
        }
        setLoading(true);
        try {
            await resetPassword({ token, new_password: password });
            setSuccess(true);
        } catch (err) {
            setError(err?.response?.data?.detail || "Could not reset password. The link may have expired!");
        } finally {
            setLoading(false);
        }
    };

    if (!token) {
        return (
            <Box maxWidth={400} mx="auto" mt={8}>
                <Alert severity="error">Invalid or missing reset token.</Alert>
            </Box>
        );
    }

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
                Reset Password
            </Typography>
            {success ? (
                <>
                    <Alert severity="success" sx={{ mb: 2 }}>
                        Password has been changed! You may now log in.
                    </Alert>
                    <Button
                        component={RouterLink}
                        to="/login"
                        variant="outlined"
                        color="primary"
                        fullWidth
                    >
                        Go to Login
                    </Button>
                </>
            ) : (
                <form onSubmit={handleSubmit}>
                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                    <TextField
                        label="New Password"
                        type="password"
                        value={password}
                        fullWidth
                        margin="normal"
                        onChange={e => setPassword(e.target.value)}
                        required
                    />
                    <TextField
                        label="Confirm New Password"
                        type="password"
                        value={confirmPassword}
                        fullWidth
                        margin="normal"
                        onChange={e => setConfirmPassword(e.target.value)}
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
                        {loading ? <CircularProgress size={24} /> : "Reset Password"}
                    </Button>
                </form>
            )}
        </Box>
    );
}