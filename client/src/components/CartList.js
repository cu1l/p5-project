import React from "react";
import CartCard from './CartCard'
import Box from '@mui/material/Box';


function CartList({ cartL, user }) {
    const cartTable = cartL.map((cartObj) => {
        return (
        <Box
              display="flex"
              justifyContent="center"
              alignItems="center"
              spacing={1}
        > 
        <CartCard key={cartObj.id} cartObj={cartObj} user={user}></CartCard>
        </Box>
        )
      })
    return (
        <Box
          justifyContent="center"
          alignItems="center"
          sx={{
            minWidth: '250px',
            display: 'grid',
            gridTemplateColumns: 'repeat(6, 5fr)',
            gap: '20px',
            p: '5px',
          }}>
        {cartTable}
        </Box>
    )        
}

export default CartList