import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useHistory } from "react-router-dom";
import Link from '@mui/material/Link';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Stack from '@mui/material/Stack';

const darkTheme = createTheme({
    palette: {
      mode: 'dark',
    },
  });

export default function Login({ setUser }) {
  const history = useHistory();
  function handleSignup() {
    history.push('/signup');
  }
  const handleSubmit = (event) => {
    const data = new FormData(event.currentTarget);
    const enteredUser = {
      username: data.get('username'),
      password: data.get('password'),
    }
    fetch('/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(enteredUser),
  })
  .then(res => {
    if (res.ok){
      res.json().then(setUser(enteredUser))
      console.log("Logged in!")
    }
    else{
      return(
      <Stack sx={{ width: '100%' }} spacing={2}>
        <Alert severity="error">
          <AlertTitle>Error</AlertTitle>
          Invalid User
        </Alert>
      </Stack>
      )
    }
  })
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <Container component="main" maxWidth="xs" sx={{
        mt: 50,
        border: 1,
        borderColor: 'grey.500',
        borderRadius: '16px'
      }}> 
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            boarder: 1,
            borderColor: 'grey.500',
          }}
        >
          <Typography component="h1" variant="h5" sx={{mt: -5}}>
            Sign in
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Link sx={{alignItems: 'center'}} href="#" onClick={handleSignup}>No Account? Click Here!</Link>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
