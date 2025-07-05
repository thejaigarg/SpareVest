// src/pages/BankAccount.jsx
import React, { useState } from "react";
import {
  Box, Typography, List, ListItem, ListItemText, Divider,
  CircularProgress, Alert, TextField, Button, MenuItem
} from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import { createBankAccount } from "../api/bankAccount";
import { useBankAccounts } from "../hooks/useBankAccounts";

export default function BankAccount() {
  const { token, user } = useAuth();
  const allowedCurrency = user?.currency || "USD";
  const { accounts, loading, error, refresh } = useBankAccounts(token);
  const [form, setForm] = useState(
    { 
      bank_name: "", 
      account_number: "",
      currency: allowedCurrency,
    }
  );
  const [submitError, setSubmitError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async e => {
    e.preventDefault();
    setSubmitError("");
    setSubmitting(true);
    try {
      await createBankAccount(token, form);
      setForm({ bank_name: "", account_number: "" });
      refresh();
    } catch (err) {
      setSubmitError(err.response?.data?.detail || err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (!token) {
    return <Alert severity="warning">Please log in.</Alert>;
  }
  if (loading) {
    return <CircularProgress sx={{ mt: 8 }} />;
  }

  return (
    <Box p={4} maxWidth={600} mx="auto">
      <Typography variant="h4" gutterBottom>
        Your Bank Accounts
      </Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {accounts.length === 0 ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          No bank accounts on file.
        </Alert>
      ) : (
        <List disablePadding sx={{ mb: 4 }}>
          {accounts.map(a => (
            <React.Fragment key={a.id}>
              <ListItem>
                <ListItemText
                  primary={a.bank_name}
                  secondary={`•••• ${a.account_number.slice(-4)}`}
                />
              </ListItem>
              <Divider component="li" />
            </React.Fragment>
          ))}
        </List>
      )}
      <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection="column" gap={2}>
        <Typography variant="h6">Link a New Bank Account</Typography>
        {submitError && <Alert severity="error">{submitError}</Alert>}
        <TextField
          label="Bank Name"
          value={form.bank_name}
          onChange={e => setForm(f => ({ ...f, bank_name: e.target.value }))}
          required
        />
        <TextField
          label="Account Number"
          value={form.account_number}
          onChange={e => setForm(f => ({ ...f, account_number: e.target.value }))}
          required
        />
        <TextField
          select
          label="Currency"
          value={form.currency}
          onChange={e => setForm(f => ({ ...f, currency: e.target.value }))}
          required
          margin="normal"
          disabled  // <--- Disable for now, enable later for multi-currency
        >
          <MenuItem value={allowedCurrency}>{allowedCurrency}</MenuItem>
        </TextField>
        <Button type="submit" variant="contained" disabled={submitting}>
          {submitting ? "Linking…" : "Link Account"}
        </Button>
      </Box>
    </Box>
  );
}
