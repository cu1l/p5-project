import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';

import { useHistory } from "react-router-dom";

export default function OutlinedCartCard({ cartObj, user }) {
  const history = useHistory();
  const {id, cart_entry_id, image, name, price, inventory} = cartObj
  const handleRemoveFromCart = (event) => {
    event.preventDefault();
    
    fetch(`/cart/${cart_entry_id}`, { method: "DELETE" })
      .then((r) => {
        if (r.ok) {
          console.log("Removed item from cart!")
        }
      })

    history.push('/cart');
    history.go(0) // refresh
  };

  return (
    <Box sx={{ Width: 250 }}>
      <FormControl>
      <Card variant="outlined" style={{ minWidth: "350px", maxWidth: "350px" }}>
        <CardContent>
          <CardMedia
            component="img"
            height="194"
            image={image}
            alt="item"
          />
          <Typography variant="h5" component="div">
            {name}
          </Typography>
          <Typography color="text.secondary">
            Price: ${Math.round(price).toFixed(2)}
          </Typography>
        </CardContent>
        <CardActions>
          <Button variant="contained" onClick={handleRemoveFromCart}>Delete</Button>
        </CardActions>
      </Card>
      </FormControl>
    </Box>
  );
}