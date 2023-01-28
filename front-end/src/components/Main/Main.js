import React from 'react'
import { Routes, Route } from 'react-router-dom';
import Login from '../Login/Login';
import Products from '../Products/Products';
import PrivateRoute from './PrivateRoute';

const Main = () => {
   const [isAuthenticated, setLoggedin] = React.useState(false);

   const login = () => {
      setLoggedin(true);
      console.log("You are authenticated")
   };

   const logout = () => {
      setLoggedin(false);
   };

   return (
      <main>
         <Routes>
            <Route path="/" element={<Login login={login} />} />
            <Route
               path="/products"
               element={
                  <PrivateRoute isAuthenticated={isAuthenticated}>
                     <Products />
                  </PrivateRoute>
               }
            />
         </Routes>
      </main>
   )
}

export default Main