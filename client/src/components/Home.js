import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';

import { useHistory } from "react-router-dom";

function Home(){
    const history = useHistory();
    function handleClick() {
        history.push('/listings/new')
    }
    return (
        <Box>
            <Button variant="contained" onClick={handleClick}>Create New Listing</Button>
        </Box>
    )
}

export default Home