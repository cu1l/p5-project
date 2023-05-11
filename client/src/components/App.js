import * as React from 'react';
import { Switch, Route, } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useHistory } from "react-router-dom";
import { RecoilRoot } from "recoil";

import Login from './Login'
import Navbar from './Navbar'
import SignUp from './SignUp'
import ItemList from './ItemList'
import Profile from  './Profile'
import NewItem from './NewItem'
import Home from './Home'
import Cart from './Cart'
import EditProfile from './EditProfile'
import Verify from './Verify'

//material imports
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  const history = useHistory();
  const [user, setUser] = useState();
  const [items, setItems] = useState([]);
  const [itemSearch, setSearch] = useState("")
  const [cart, setCart] = useState([])

  console.log(itemSearch)

  const handleLogout = () => {
    fetch("/logout", { method: "DELETE" })
      .then((r) => {
        if (r.ok) {
          setUser(undefined)
        }
        history.push('/login')
      })
  }

  useEffect(() => {
    fetch('/items')
    .then((r) => r.json())
    .then(setItems)
  }, []);

  useEffect(() => {
    fetch("/check_session")
      .then((r) => {
        if (r.ok) {
          r.json().then((user) => setUser(user));
          console.log(user)
        }
      });
  }, []);

  useEffect(() => {
    fetch(`/carts`)
    .then((r) => r.json())
    .then(setCart)
  }, []);

  return (
    <div style={{ width: '100%' }}>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <Navbar user={user} handleSearch={setSearch} logout={handleLogout}/>
        <Switch>
          <Route exact path='/home'><Home /></Route>
          <Route exact path='/signup'><SignUp setUser={setUser}/></Route>
          <Route exact path='/login'><Login setUser={setUser}/></Route>
          {user && cart.length !== 0 ? <Route exact path='/cart'><Cart carts={cart} user={user}/></Route> : 0}
          <Route exact path='/profile'><Profile user={user} logout={handleLogout}/></Route>
          <Route exact path='/profile/edit'><EditProfile user={user} setUser={setUser}/></Route>
          <Route exact path='/listings'><ItemList itemL={items.filter(items => items.name.toLowerCase().includes(itemSearch.toLowerCase()))} user={user}></ItemList></Route>
          <Route exact path='/listings/new'><NewItem user={user}/></Route>
          <Route exact path='/verify'><Verify user={user} setUser={setUser}/></Route>
        </Switch>
      </ThemeProvider>
    </div>
  );
}

export default App;