// src/api/auth.js
import axios from "axios";
import { API_BASE_URL } from "../constants/appConfig";

// Backend expects: POST /auth/token with form data (username, password)
export async function login(email, password) {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);

  const response = await axios.post(`${API_BASE_URL}/auth/token`, params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return response.data; // { access_token, token_type }
}
