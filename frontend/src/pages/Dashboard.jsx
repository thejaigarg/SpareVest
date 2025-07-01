// src/components/Dashboard.jsx
import React, { useEffect, useState } from "react";
import { Box, Typography, Button, CircularProgress } from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function Dashboard() {
  const { token, user } = useAuth();
  const navigate = useNavigate();

  // Derive hasBankAccount straight from your context user object
  const hasBankAccount = Array.isArray(user?.bankAccounts) && user.bankAccounts.length > 0;

  const [loadingTx, setLoadingTx] = useState(true);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    if (!token || !hasBankAccount) {
      setLoadingTx(false);
      return;
    }

    const api = axios.create({
      baseURL: process.env.REACT_APP_API_URL,
      headers: { Authorization: `Bearer ${token}` },
    });

    api
      .get("/transactions")
      .then(res => setTransactions(res.data))
      .catch(err => console.error("Error fetching transactions:", err))
      .finally(() => setLoadingTx(false));
  }, [token, hasBankAccount]);

  // If you want to show a spinner while tx are loading…
  if (loadingTx) {
    return (
      <Box display="flex" justifyContent="center" mt={8}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Welcome back, {user?.firstName || "there"}!
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
        <Box>
          {/* — Your Figma‐inspired header here — */}
          <Box textAlign="center" mb={4}>
            <Typography variant="h2">${user.totalBalance.toFixed(2)}</Typography>
            <Typography color="textSecondary">Total Balance</Typography>
            {/* progress bar, “Add Transaction” & “Transfer Now” buttons… */}
          </Box>

          {/* Recent Transactions */}
          <Box mt={6}>
            <Typography variant="h6" gutterBottom>
              Recent Transactions
            </Typography>
            {transactions.length === 0 ? (
              <Typography color="textSecondary">No transactions yet.</Typography>
            ) : (
              transactions.map(tx => (
                <Box
                  key={tx.id}
                  display="flex"
                  justifyContent="space-between"
                  alignItems="center"
                  p={2}
                  mb={1}
                  bgcolor="#fff"
                  borderRadius={2}
                  boxShadow={1}
                >
                  <Box>
                    <Typography>{tx.merchantName}</Typography>
                    <Typography variant="caption" color="textSecondary">
                      {new Date(tx.timestamp).toLocaleString()}
                    </Typography>
                  </Box>
                  <Typography color="success.main">
                    +${tx.amount.toFixed(2)}
                  </Typography>
                </Box>
              ))
            )}
          </Box>
        </Box>
      )}
    </Box>
  );
}
