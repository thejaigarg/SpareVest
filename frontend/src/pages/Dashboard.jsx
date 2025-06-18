import { Container, Typography, Button, Box } from '@mui/material';

export default function Dashboard() {
  return (
    <Box
      sx={{
        bgcolor: 'background.default',
        minHeight: '100vh',
        color: 'text.primary',
        py: 6,
        px: 2,
      }}
    >
      <Container maxWidth="sm">
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Button variant="contained" color="primary">
          Dark Mode Button
        </Button>
      </Container>
    </Box>
  );
}
