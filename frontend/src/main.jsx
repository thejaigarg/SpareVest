import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { getTheme } from './styles/theme.js';
import { BrowserRouter } from 'react-router-dom';

const darkTheme = getTheme('dark');

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <BrowserRouter> {/* ✅ Fix: Wrap App with Router */}
        <App />
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);
