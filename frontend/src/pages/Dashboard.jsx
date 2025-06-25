// src/pages/dashboard.jsx
import React, { useEffect, useState } from "react";
import { Container, Typography, Box, Button } from "@mui/material";
import { getCurrentUser } from "../api/auth";
import { useAuth } from "../hooks/useAuth";

export default function Dashboard() {
  const { token } = useAuth();
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      getCurrentUser(token)
        .then(setUser)
        .catch(() => setUser(null));
    }
  }, [token]);

  return (
    <Box
      sx={{
        bgcolor: "background.default",
        minHeight: "100vh",
        color: "text.primary",
        py: 6,
        px: 2,
      }}
    >
      <Container maxWidth="sm">
        <Typography variant="h4" gutterBottom>
          {user ? `Hello, ${user.full_name || user.email}` : "Welcome!"}
        </Typography>
        <Typography variant="body1" sx={{ mb: 4 }}>
          This is your investment overview. More features coming soon!
        </Typography>
        <Button variant="contained" color="primary" disabled>
          Coming Soon: Portfolio Visualization
        </Button>
      </Container>
    </Box>
  );
}
