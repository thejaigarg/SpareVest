// src/pages/BankAccount.jsx
import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  CircularProgress,
  List,
  ListItem,
} from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import axios from "axios";

export default function BankAccount() {
  const { token } = useAuth();
  const [accounts, setAccounts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) {
      setError("No auth token");
      setLoading(false);
      return;
    }

    const fetchAccounts = async () => {
      try {
        const response = await axios.get("http://localhost:8000/bank-accounts/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setAccounts(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to fetch bank accounts");
      } finally {
        setLoading(false);
      }
    };

    fetchAccounts();
  }, [token]);

  return (
    <Box p={4} maxWidth={600} mx="auto">
      <Typography variant="h4" gutterBottom>
        Your Bank Accounts
      </Typography>

      {loading ? (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error" mb={2}>
          Error: {error}
        </Typography>
      ) : !Array.isArray(accounts) ? (
        <Typography>No data to display.</Typography>
      ) : accounts.length === 0 ? (
        <Typography>You have no bank accounts.</Typography>
      ) : (
        <List>
          {accounts.map((acct) => (
            <ListItem key={acct.id}>
              {acct.bank_name} ••••{acct.account_number.slice(-4)}
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
}
