import { createTheme } from '@mui/material/styles';

const darkTheme = {
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9', // Light Blue
    },
    secondary: {
      main: '#ffb74d',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
    text: {
      primary: '#ffffff',
      secondary: '#aaaaaa',
    },
  },
  typography: {
    fontFamily: 'Inter, Roboto, sans-serif',
    h1: { fontWeight: 700 },
    h2: { fontWeight: 600 },
    h3: { fontWeight: 600 },
    button: { textTransform: 'none', fontWeight: 600 },
  },
};

export const getTheme = () => createTheme(darkTheme);
