import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import Background from './Background.jpg'
import Rating from '@mui/material/Rating';
import { useState } from 'react';

import { useHistory } from "react-router-dom";

export default function OutlinedCard({ itemObj, user }) {
  const [value, setValue] = React.useState(2);
  const history = useHistory();
  const {id, image, name, price, inventory, user_rating, user_id} = itemObj
  const handleAddToCart = (event) => {
    event.preventDefault();
    const cartItem = {
      item_id: id,
      user_id: user.id,
    }

    fetch('/carts', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(cartItem),
    })
    .then(res => {
      if (res.ok){
        console.log("Added to cart!")
      }
      else{
        alert("Failed adding to cart.")
      }
    })
  }

    // put in proper place when u add element to place review
    const handleAddRating = (e) => {
      e.preventDefault();
      const reviewItem = {
        user_id: user_id,
        reviewer_id: user.id,
        rating: value
      }
      fetch('/review', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(reviewItem),
      })
      .then(res => {
        if (res.ok){
          console.log("Added review!")
        }
      })
    };
  

  return (
    <Box sx={{ Width: 250, backgroundImage:`${Background}`}}>
      <FormControl>
      <Card variant="outlined" style={{ minWidth: "350px", maxWidth: "350px", backgroundImage:`${Background}`}}>
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
          <Typography sx={{ mb: 1.5 }} color="text.secondary">
            {inventory} in stock
          </Typography>
          <Rating
            name="simple-controlled"
            value={value}
            onChange={(event, newValue) => {
            setValue(value);
            console.log(value)
            }}
            onClick={handleAddRating}
          />
          <Typography color="text.secondary">
            User Rating: {Math.round(user_rating).toFixed(1)} / 5
          </Typography>
        </CardContent>
        <CardActions>
        <Button variant="contained" onClick={handleAddToCart}>Add To Cart</Button>
        </CardActions>
      </Card>
      </FormControl>
    </Box>
  );
}