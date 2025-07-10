// src/api/client.js
import axios from "axios";
import { API_BASE_URL } from "../constants/appConfig";

const API = axios.create({
  baseURL: API_BASE_URL,
});

// 1️⃣ If there’s a token saved already, seed it immediately
const savedToken = sessionStorage.getItem("token");
if (savedToken) {
  API.defaults.headers.common["Authorization"] = `Bearer ${savedToken}`;
}

// 2️⃣ Always read the latest token before sending any request
API.interceptors.request.use(config => {
  const token = sessionStorage.getItem("token");
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  } else {
    delete config.headers?.Authorization;
  }
  return config;
});

export function setAuthToken(token) {
  if (token) {
    sessionStorage.setItem("token", token);
    API.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    sessionStorage.removeItem("token");
    delete API.defaults.headers.common["Authorization"];
  }
}

export default API;
