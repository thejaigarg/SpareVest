// src/hooks/useRecentTransactions.js
import { useState, useCallback, useEffect } from "react";
import { listTransactions } from "../api/transaction";
import { useAuth } from "./useAuth";

// Fetches /transactions?limit=5 for the logged-in user
export function useRecentTransactions(limit = 5) {
  const { token } = useAuth();

  const [state, setState] = useState({
    transactions: null,
    loading: !!token,
    error: null,
  });

  const fetchTransactions = useCallback(() => {
    if (!token) return;
    setState(s => ({ ...s, loading: true, error: null }));
    listTransactions({ limit })
      .then(transactions => setState({ transactions, loading: false, error: null }))
      .catch(err => {
        setState({ transactions: null, loading: false, error: err?.message || "Failed to load transactions." });
      });
  }, [limit, token]);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  return {
    transactions: state.transactions,
    loading: state.loading,
    error: state.error,
    refresh: fetchTransactions,
  };
}