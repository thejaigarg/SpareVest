// src/api/auth.js
import API, { setAuthToken } from "./client";

// login → { access_token, user }
export async function login(email, password) {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);

  const { access_token } = await API.post("/auth/token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  }).then(r => r.data);

  setAuthToken(access_token);
  const user = await API.get("/users/me").then(r => r.data);
  return { access_token, user };
}

export function getCurrentUser() {
  return API.get("/users/me").then(r => r.data);
}

export async function signup(details) {
  return API.post("/users/", details).then(r => r.data);
}

export async function requestPasswordReset(email) {
  return API.post("/auth/password-reset/request", { email }).then(r => r.data);
}

// Reset password

export function resetPassword({ token, new_password }) {
  return API.post("/auth/password-reset/confirm", { token, new_password });
}