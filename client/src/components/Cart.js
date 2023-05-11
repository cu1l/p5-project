import * as React from 'react';
import CartList from './CartList'
import { Button } from '@mui/material';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import { useHistory } from "react-router-dom";

export default function Cart({ carts, user }) {
    const history = useHistory();
    const handleCheckOut = (event) => {
        event.preventDefault();
        const emailInfo = new Map(); // used to store and get info for email
        const originalInventory = new Map(); // keep track of inventory actively
        carts.forEach(item => {
            if (originalInventory.has(item.id) === false){
                const emailData = {
                  item_name: item.name,
                  item_price: item.price,
                  item_quantity: 1
                };
                
                emailInfo.set(item.id, emailData)
                originalInventory.set(item.id, item.inventory);
            }

            if (originalInventory.has(item.id)) {
              const emailData = {
                item_name: item.name,
                item_price: item.price,
                item_quantity: emailInfo.get(item.id).item_quantity + 1
              };
              
              emailInfo.set(item.id, emailData)
            }
            
            const updatedInventory = originalInventory.get(item.id) - 1;
            const newInv = {
                inventory: updatedInventory
            };

            originalInventory.set(item.id, updatedInventory);

            // update inventory value
            fetch(`/items/${item.id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newInv)})
            .then((r) => {
              if (r.ok) {
                console.log("Updated item entry!")
              }
            });

            // remove items from cart
            fetch(`/cart/${item.cart_entry_id}`, { method: "DELETE" })
            .then((r) => {
              if (r.ok) {
                console.log("Removed item from cart!");
              }
            });
        });

        // list of items purchased with prices
        let item_string = "";
        emailInfo.forEach(info => {
          item_string = item_string + info.item_name + ": " + Math.round(info.item_price).toFixed(2) + "\n";
        });
        
        // not tested should be easy to setup tho
        const data = {
          service_id: 'service_t5u78po',
          template_id: 'template_71cnsqg',
          user_id: 'NrF4lkG5aieZ04YIl',
          template_params: {
              'to_name': `${user.first_name} ${user.last_name}`,
              'items': `${item_string}`,
              'total': `${Math.round(carts[0].cart_total).toFixed(2)}`,
              'g-recaptcha-response': '03AHJ_ASjnLA214KSNKFJAK12sfKASfehbmfd...'
          }
        };
    
        fetch('https://api.emailjs.com/api/v1.0/email/send', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
        .then(res => {
          if (res.ok){
             console.log("Added to cart!")
          }
          else{
             alert("Failed adding to cart.")
          }
        })

        const receipt = {
          user_id: user.id,
          item_id: 0,
          total: Math.round(carts[0].cart_total).toFixed(2),
          items: item_string
        }

        fetch('/receipt', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(receipt),
        })
        .then(res => {
          if (res.ok){
             console.log("Added receipt!")
          }
        })
    
        history.push('/cart');
        history.go(0); // refresh

        alert("Successful Purchase.")
    };

    return (
        <>
            <CartList cartL={carts.filter(carts => carts.cart_owner_id === user.id)} user={user}></CartList>
            <TextField sx={{ml:"1.4%"}} label="Street" variant="standard" />
            <TextField sx={{ml:"1.4%"}} label="State" variant="standard" />
            <TextField sx={{ml:"1.4%"}} label="Country" variant="standard" />
            <TextField sx={{ml:"1.4%"}} label="Card Number" variant="standard" />
            <TextField sx={{ml:"1.4%"}} label="CSV" variant="standard" />
            <Typography sx={{ml:"1.4%"}} variant="h6">Total: ${Math.round(carts[0].cart_total).toFixed(2)}</Typography>
            <Button sx={{ml:"1.4%"}} variant="contained" onClick={handleCheckOut}>Check Out</Button>
        </>
    );
 }