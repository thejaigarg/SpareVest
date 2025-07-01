// src/api/bankAccount.js
import API from "./client";

export async function listBankAccounts() {
  return API.get("/bank-accounts")
    .then(r => (Array.isArray(r.data) ? r.data : []));
}

export async function createBankAccount({ bank_name, account_number }) {
  return API.post("/bank-accounts", { bank_name, account_number })
    .then(r => r.data);
}
