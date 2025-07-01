import axios from "axios";
import { API_BASE_URL } from "../constants/appConfig";

function client(token) {
  return axios.create({
    baseURL: API_BASE_URL,
    headers: { Authorization: `Bearer ${token}` },
  });
}

/**
 * GET /bank-accounts → list of BankAccountInDB
 */
export async function listBankAccounts(token) {
  const res = await client(token).get("/bank-accounts");
  return Array.isArray(res.data) ? res.data : [];
}

/**
 * POST /bank-accounts with { bank_name, account_number }
 */
export async function createBankAccount(token, { bank_name, account_number }) {
  const res = await client(token).post("/bank-accounts", {
    bank_name,
    account_number,
  });
  return res.data;
}
