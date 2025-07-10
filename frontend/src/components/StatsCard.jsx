import React from "react";
import { Box, Typography, Paper } from "@mui/material";

// Optionally pass 'icon' as a child
export default function StatsCard({ title, value, subtitle, icon, color = "primary.main", valueColor = "inherit" }) {
  return (
    <Paper
      sx={{
        borderRadius: 2,
        p: 3,
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 200,
        boxShadow: 1,
        bgcolor: "white",
        flex: 1,
      }}
    >
      {icon && (
        <Box mb={1} color={color} fontSize={26}>
          {icon}
        </Box>
      )}
      <Typography variant="h5" fontWeight={700} color={valueColor}>
        {value}
      </Typography>
      <Typography variant="subtitle2" color="textSecondary" fontWeight={600}>
        {title}
      </Typography>
      {subtitle && (
        <Typography variant="body2" color="textSecondary">
          {subtitle}
        </Typography>
      )}
    </Paper>
  );
}