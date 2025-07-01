// src/hooks/useBankAccounts.js
import { useState, useEffect, useCallback } from "react";
import { listBankAccounts } from "../api/bankAccount";
import { useAuth } from "./useAuth";

export function useBankAccounts() {
  const { token } = useAuth();
  const [state, setState] = useState({
    accounts: null,
    loading: !!token,
    error: null,
  });

  const fetchAccounts = useCallback(() => {
    if (!token) return;
    setState(s => ({ ...s, loading: true, error: null }));
    listBankAccounts()
      .then(accounts => setState({ accounts, loading: false, error: null }))
      .catch(err => setState({ accounts: [], loading: false, error: err.message }));
  }, [token]);

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  return { 
    accounts: state.accounts, 
    loading: state.loading, 
    error: state.error, 
    refresh: fetchAccounts 
  };
}
