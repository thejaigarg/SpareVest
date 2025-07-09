// src/pages/Dashboard.jsx
import React from "react";
import { Box, Typography, Button, CircularProgress, Alert } from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";
import { useBankAccounts } from "../hooks/useBankAccounts";
import { usePortfolio } from "../hooks/usePortfolio";
import BalanceGoalProgress from "../components/BalanceProgressBar";

export default function Dashboard() {
  const { token, user } = useAuth();
  const navigate = useNavigate();
  const { accounts = [], loading, error, refresh } = useBankAccounts();
  const { summary, loading: portfolioLoading, error: portfolioError, refresh: refreshPortfolio } = usePortfolio();

  if (!token) {
    // Not logged in: this is a protected route, but just in case.
    return (
      <Box p={4}>
        <Alert severity="warning">
          Please log in to view your dashboard.
        </Alert>
      </Box>
    );
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={8}>
        <CircularProgress />
      </Box>
    );
  }

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

  // Show ONLY add bank account prompt if none are linked
  if (!accounts || accounts.length === 0) {
    return (
      <Box minHeight="60vh" display="flex" alignItems="center" justifyContent="center">
        <Box textAlign="center">
          <Typography variant="h5" gutterBottom>
            You don’t have a bank account linked yet.
          </Typography>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate("/profile/bank-account")}
          >
            Add Bank Account
          </Button>
        </Box>
      </Box>
    );
  }

if (portfolioLoading) {
  return (
    <Box display="flex" justifyContent="center" mt={8}>
      <CircularProgress />
    </Box>
  );
}

if (portfolioError) {
  return (
    <Box p={4}>
      <Alert severity="error">
        Error loading portfolio: {portfolioError}
        <Box mt={2}>
          <Button variant="outlined" onClick={refreshPortfolio}>
            Retry
          </Button>
        </Box>
      </Alert>
    </Box>
  );
}

// -- Render top card once portfolio loaded
return (
  <Box p={{ xs: 2, sm: 4 }}>
    <BalanceGoalProgress
      balance={summary.sparevest_balance}
      roundupBucket={summary.roundup_bucket}
      savingsGoal={summary.savings_goal}
      percentToGoal={Math.round(summary.percent_to_goal)}
      currency={user.currency}
      onAddTransaction={() => {}} // will add next!
      onTransferNow={() => {}}    // will add next!
    />
    {/* Next: stats row, and recent transactions */}
    {/* ... */}
  </Box>
);
}