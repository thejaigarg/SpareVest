import { useState, useCallback, useEffect } from "react";
import { getPortfolioSummary } from "../api/portfolio";
import { useAuth } from "./useAuth";

export function usePortfolio(){
    const { token } = useAuth();

    const [state, setState] = useState({
        summary: null,
        loading: !!token,
        error: null,
    });

    const fetchPortfolio = useCallback(() => {
        if (!token) return;
        setState(s => ({ ...s, loading: true, error: null}));
        getPortfolioSummary()
            .then(summary => setState({ summary, loading: false, error: null}))
            .catch(err => {
                setState({ summary: null, loading: false, error:err?.message || "Failed to load portfolio"});
            });
    }, [token]);
    
    useEffect(() => {
        fetchPortfolio();
    }, [fetchPortfolio]);

    return{
        summary: state.summary,
        loading: state.loading,
        error: state.error,
        refresh: fetchPortfolio
    };
    
}