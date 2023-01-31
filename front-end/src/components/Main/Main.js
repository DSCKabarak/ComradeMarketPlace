import React from 'react'
import { Routes, Route } from 'react-router-dom';
import Login from '../Login/Login';
import Products from '../Products/Products';

const Main = () => {

   return (
      <main>
         <Routes>
            <Route path="/login" element={<Login />} />
            <Route
               path="/"
               element={<Products />}
            />
         </Routes>
      </main>
   )
}

export default Main