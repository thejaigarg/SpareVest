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

  const { access_token, token_type } = response.data;
  
  // Store token in sessionStorage
  sessionStorage.setItem("token", access_token);
  sessionStorage.setItem("token_type", token_type);

  // Fetch current user details using the token
  const userResponse = await axios.get(`${API_BASE_URL}/users/me`, {
    headers: { Authorization: `Bearer ${access_token}` },
  });

  const userData = userResponse.data;

  // Store the current user in sessionStorage
  sessionStorage.setItem("user", JSON.stringify(userData));

  return { access_token, user: userData };
}

// Registers a new user
export async function signup({ email, full_name, password }) {
  const response = await axios.post(`${API_BASE_URL}/users/`, {
    email,
    full_name,
    password,
  });
  return response.data;
}

export async function getCurrentUser(token) {
  const response = await axios.get(`${API_BASE_URL}/users/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data; // { email, full_name, id, is_active }
}

export async function requestPasswordReset(email) {
  const response = await axios.post(`${API_BASE_URL}/auth/password-reset/request`, { email });
  return response.data;
}
