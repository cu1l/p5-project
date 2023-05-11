import React from "react";
import Card from './Card';
import Box from '@mui/material/Box';


function ItemList({ itemL, user }) {
    const itemTable = itemL.map((itemObj) => {
        return (
        <Box
              display="flex"
              justifyContent="center"
              alignItems="center"
              spacing={1}
        > 
        <Card key={itemL.id} itemObj={itemObj} user={user}></Card>
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
        {itemTable}
        </Box>
    )        
}

export default ItemList