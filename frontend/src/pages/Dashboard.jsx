// src/components/Dashboard.jsx
import React from "react";
import { Box, Typography, Button, CircularProgress, Alert } from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";
import { useBankAccounts } from "../hooks/useBankAccounts";

export default function Dashboard() {
  const { token, user } = useAuth();
  const navigate = useNavigate();
  const { accounts, loading, error, refresh } = useBankAccounts(token);

  // guard: not authenticated
  if (!token) {
    return (
      <Box p={4}>
        <Alert severity="warning">Please log in to view your dashboard.</Alert>
      </Box>
    );
  }

  // loading bank accounts
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={8}>
        <CircularProgress />
      </Box>
    );
  }

  // error fetching banks
  if (error) {
    return (
      <Box p={4}>
        <Alert severity="error">
          Error loading bank accounts: {error}
          <Box mt={2}>
            <Button variant="outlined" onClick={refresh}>
              Retry
            </Button>
          </Box>
        </Alert>
      </Box>
    );
  }

  const hasBankAccount = Array.isArray(accounts) && accounts.length > 0;

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Welcome back, {user?.full_name || "there"}!
      </Typography>

      {!hasBankAccount ? (
        <Box textAlign="center" my={6}>
          <Typography variant="h6" color="textSecondary" gutterBottom>
            You don’t have a bank account linked yet.
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate("/profile/bank-account")}
          >
            Add Bank Account
          </Button>
        </Box>
      ) : (
        <Box textAlign="center" my={6}>
          <Typography variant="h6">
            You have {accounts.length} linked bank{" "}
            {accounts.length === 1 ? "account" : "accounts"}.
          </Typography>
          <Box mt={4}>
            <Button
              variant="contained"
              color="primary"
              onClick={() => navigate("/profile/bank-account")}
            >
              Manage Bank Accounts
            </Button>
          </Box>
        </Box>
      )}
    </Box>
  );
}
