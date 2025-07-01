// src/hooks/useBankAccounts.js
import { useState, useEffect } from "react";
import { listBankAccounts } from "../api/bankAccount";

let cache = null;
let errorCache = "";
let loading = false;
let subscribers = [];

function notify() {
  subscribers.forEach(cb => cb({ accounts: cache, loading, error: errorCache }));
}

export function useBankAccounts(token) {
  const [state, setState] = useState({
    accounts: cache,
    loading: token && cache === null,
    error: errorCache,
  });

  useEffect(() => {
    const cb = newState => setState(newState);
    subscribers.push(cb);

    if (cache === null && token && !loading) {
      loading = true;
      notify();
      listBankAccounts(token)
        .then(list => {
          cache = list;
          errorCache = "";
        })
        .catch(err => {
          cache = [];
          errorCache = err.message || "Failed to load";
        })
        .finally(() => {
          loading = false;
          notify();
        });
    } else {
      notify();
    }

    return () => {
      subscribers = subscribers.filter(fn => fn !== cb);
    };
  }, [token]);

  const refresh = () => {
    if (!token) return;
    loading = true;
    notify();
    listBankAccounts(token)
      .then(list => {
        cache = list;
        errorCache = "";
      })
      .catch(err => {
        cache = [];
        errorCache = err.message || "Failed to load";
      })
      .finally(() => {
        loading = false;
        notify();
      });
  };

  return { ...state, refresh };
}
