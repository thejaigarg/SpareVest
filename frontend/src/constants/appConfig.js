// src/constants/appConfig.js
console.log("❯ API_BASE_URL is:", import.meta.env.VITE_API_BASE_URL);
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";
