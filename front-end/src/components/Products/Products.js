import React from 'react'
import { Link } from 'react-router-dom';

const Products = () => {
  const userString = sessionStorage.getItem("user");
  const user = JSON.parse(userString);

  return (

    <div onClick={() => {
      sessionStorage.setItem("user", null);
      window.location.reload()}}>Welcome to KabuShop {user ? `, ${user.first_name}` : <Link to="/login">Login</Link>}</div>
  )
}

export default Products