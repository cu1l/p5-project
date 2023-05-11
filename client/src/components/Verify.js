import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useHistory } from "react-router-dom";

import TextEditor from './TextEditor';

const darkTheme = createTheme({
    palette: {
      mode: 'dark',
    },
  });

export default function EditProfile({ user, setUser }) {
    const history = useHistory();
    const handleSubmit = (event) => {
      event.preventDefault();
      const new_data = {
        verified: 1
      };
  
      console.log(new_data)
      fetch(`/user/${user.id}`, {
          method: 'PATCH',
          headers: {
              'Content-Type': 'application/json',
          },
              body: JSON.stringify(new_data),
          })
      .then((res) => {
              if (res.ok) {
                return res.json();
              }
              throw new Error('Network response was not ok');
            })
            .then((new_data) => {
              setUser(new_data);
              setUser(undefined)
              history.push('/login')
            })
            .catch((error) => {
              console.error(error);
            });
        };
  
    return (
      <ThemeProvider theme={darkTheme}>
        <Container component="main" maxWidth="xs" sx={{
          mt: 50
        }}>
          <CssBaseline />
          <Box
            sx={{
              marginTop: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography>Why would you like to be verified?</Typography>
            <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <TextEditor></TextEditor>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                onClick={handleSubmit}
                sx={{ mt: 3, mb: 2 }}
              >
                Verify!
              </Button>
              <Grid container justifyContent="flex-end">
              </Grid>
            </Box>
          </Box>
        </Container>
      </ThemeProvider>
    );
  }