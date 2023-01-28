import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import bgImage from "../../assets/login-page-bg.png";
import "./login.css";
import Modal from 'react-bootstrap/Modal';



const Login = (props) => {

   const [loginFormData, setLoginFormData] = useState({
      email: "",
      password: ""
   })

   const [registerFormData, setRegisterFormData] = useState({
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      bio: "Just a normal user",
      user_type: "buyer"
   });

   const [show, setShow] = useState(false);

   const handleClose = () => setShow(false);
   const handleShow = () => setShow(true);

   function handleLoginFormChange(e) {
      let { name, value } = e.target;
      setLoginFormData((prevFormData) => ({
         ...prevFormData,
         [name]: value
      }))
      console.log(loginFormData);
   }

   function handleOnChange(e) {
      let { name, value } = e.target;
      setRegisterFormData((prevFormData) => ({
         ...prevFormData,
         [name]: value
      }))
   }

   function handleSubmitLoginForm(e) {
      e.preventDefault();

      fetch("http://127.0.0.1:8000/comrade-market-place/api/auth/login", {
         method: 'POST',
         body: JSON.stringify(loginFormData),
         headers: {
            'Content-Type': 'application/json'
         }
      })
         .then(res => res.json())
         .then(data => {
            console.log(data);
            props.login();
            return <Navigate to="/products" replace />
         })
         .catch(err => console.log(err))
   }

   function handleOnSubmit(e) {
      e.preventDefault();

      fetch("http://127.0.0.1:8000/comrade-market-place/api/auth/register", {
         method: 'POST',
         body: JSON.stringify(registerFormData),
         headers: {
            'Content-Type': 'application/json'
         }
      })
         .then(res => res.json())
         .then(data => {
            console.log(data);
         })
         .catch(err => console.log(err))
   }

   return (
      <>
         <Modal show={show} className="modal__backdrop" onHide={handleClose}>
            <Modal.Header className="modal__header" closeButton>
               <Modal.Title>Login</Modal.Title>
            </Modal.Header>
            <Modal.Body>
               <form onSubmit={handleSubmitLoginForm}>
                  <div className="row g-3">
                     <div className="col-12">
                        <label className="visually-hidden" htmlFor="email" >Email address</label>
                        <input type="text" name="email" className="form-control form-control-sm mr-1" id="email" placeholder="name@gmail.com" value={loginFormData.email} onChange={handleLoginFormChange} />
                     </div>
                     <div className="col-12">
                        <label className="visually-hidden" htmlFor="password">Password</label>
                        <input type="password" name="password" className="form-control form-control-sm mr-1" id="password" placeholder="Password" value={loginFormData.password} onChange={handleLoginFormChange} />
                     </div>
                  </div>
                  <hr />
                  <div className="mt-3 d-flex justify-content-between gap-2">
                     <button className="bg-secondary text-white login-page__button" onClick={handleClose}>Close</button>
                     <button className="login-page__button" onClick={handleClose}>Sign In</button>
                  </div>
               </form>

            </Modal.Body>
         </Modal>
         <div className="login-page" style={{
            backgroundImage: `url(${bgImage})`,
            backgroundRepeat: "no-repeat",
            backgroundSize: "60% auto",
            backgroundPosition: "right 50% top 40%"
         }}>
            <section className="login-page__header">

               <h1>Kabu <span id="login-page__shop">Shop</span></h1>
               <p>Already a member? <span id="login-page__sign-in-link" onClick={handleShow} >sign in</span></p>
            </section >


            <h2 className="center">Create an account</h2>
            <section className="login-page__body">

               <form onSubmit={handleOnSubmit} className="login-page__form">
                  <div className="login-page__form-names">
                     <input type="text" name="first_name" id="first_name" placeholder="First Name" value={registerFormData.first_name} onChange={handleOnChange} className="login-page__form-input" />
                     <input type="text" name="last_name" id="last_name" placeholder="Last Name" value={registerFormData.last_name} onChange={handleOnChange} className="login-page__form-input" />
                  </div>
                  <input type="email" name="email" id="email" placeholder="Email" value={registerFormData.email} onChange={handleOnChange} className="login-page__form-input" />
                  <input type="password" name="password" id="password" placeholder="Password" value={registerFormData.password} onChange={handleOnChange} className="login-page__form-input" />

                  <p className="d-none d-md-block login-page__policy">
                     By Creating an account, you agree to our <span className="login-page__user-agreement">User Agreement- opens in new window
                        or tab</span> and acknowledge reading our <span className="login-page__user-agreement">User Privacy Notice- opens in new window or tab</span>.
                  </p>
                  <p className="d-md-none center login-page__policy text-lg">
                     By Creating an account, you agree to our <span className="login-page__user-agreement">Terms & Policies</span>.
                  </p>
                  <div className="login-page__btn-div">
                     <button className="login-page__button">Create Account</button>
                  </div>
               </form>
               <div className="or">
                  <span className="login-page__or">or</span>
               </div>
               <div className="login-page__oauth">
                  <div className="login-page__oauth-google"><i className="fa-brands fa-google text-primary"></i>{" "}Continue with Google</div>
               </div>
            </section>
            <div className="login-page__circle"></div>
         </div>
      </>
   )
}

export default Login;