// src/api/client.js
import axios from "axios";
import { API_BASE_URL } from "../constants/appConfig";

const API = axios.create({
  baseURL: API_BASE_URL,
});

export function setAuthToken(token) {
  if (token) {
    API.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete API.defaults.headers.common["Authorization"];
  }
}

export default API;

