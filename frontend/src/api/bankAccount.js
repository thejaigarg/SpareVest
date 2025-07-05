// src/api/bankAccount.js
import API from "./client";

export async function listBankAccounts() {
  return API.get("/bank-accounts")
    .then(r => (Array.isArray(r.data) ? r.data : []));
}

export async function createBankAccount(token, { bank_name, account_number, currency }) {
  return API.post(
    "/bank-accounts", 
    { bank_name, account_number, currency },
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )
    .then(r => r.data);
}
