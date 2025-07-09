// src/components/BalanceGoalProgress.jsx
import React from "react";
import { Box, Typography, LinearProgress, Button, Stack } from "@mui/material";
import { getCurrencySymbol } from "../utils/currencySymbol";

export default function BalanceGoalProgress({
  balance,
  roundupBucket,
  savingsGoal,
  percentToGoal,
  currency,
  onAddTransaction,
  onTransferNow,
  disableActions = false,
  loadingActions = false,
}) {
  const symbol = getCurrencySymbol(currency);

  return (
    <Box sx={{
      bgcolor: "white",
      borderRadius: 3,
      boxShadow: 1,
      p: { xs: 3, sm: 4 },
      mb: { xs: 4, sm: 6 },
      textAlign: "center"
    }}>
      <Typography variant="h3" fontWeight={700}>
        {symbol}{Number(balance).toLocaleString()}
      </Typography>
      <Typography color="text.secondary" fontWeight={600} gutterBottom>
        Total Balance
      </Typography>
      
      {/* Progress line: "$X of $Goal" and percent */}
      <Box
        display="flex"
        alignItems="center"
        justifyContent="space-between"
        mt={2} mb={1}
      >
        <Typography variant="body2">
          {symbol}{Math.round(roundupBucket)} of {symbol}{Math.round(savingsGoal)}
        </Typography>
        <Typography variant="body2" color="primary" sx={{ fontWeight: 600 }}>
          {percentToGoal || 0}%
        </Typography>
      </Box>

      {/* Progress bar */}
      <LinearProgress
        variant="determinate"
        value={Math.min(100, percentToGoal || 0)}
        sx={{
          height: 10,
          borderRadius: 5,
          backgroundColor: "#e5e7eb",
          "& .MuiLinearProgress-bar": {
            backgroundColor: "#6366f1"
          }
        }}
      />

      {/* Button Row */}
      <Stack direction="row" spacing={2} justifyContent="center" mt={3}>
        <Button
          variant="contained"
          size="large"
          sx={{ bgcolor: "#6366f1", ":hover": { bgcolor: "#4f46e5" } }}
          onClick={onAddTransaction}
          disabled={disableActions || loadingActions}
        >
          + Add Transaction
        </Button>
        <Button
          variant="outlined"
          size="large"
          sx={{ borderColor: "#6366f1", color: "#6366f1", ":hover": { borderColor: "#4f46e5", color: "#4f46e5" } }}
          onClick={onTransferNow}
          disabled={disableActions || loadingActions}
        >
          ⟳ Transfer Now
        </Button>
      </Stack>
    </Box>
  );
}