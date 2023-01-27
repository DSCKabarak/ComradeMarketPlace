import React, { useState } from "react";
import bgImage from "../../assets/login-page-bg.png";
import "./login.css";

const Login = () => {
   const [loginFormData, setLoginFormData] = useState({
      firstName: "",
      lastName: "",
      email: "",
      password: ""
   });

   function handleOnChange(e) {
      let { name, value } = e.target;
      setLoginFormData((prevFormData) => ({
         ...prevFormData,
         [name]: value
      }))
   }

   function handleOnSubmit(e) {
      e.preventDefault();
      alert(JSON.stringify(loginFormData))
   }

   return (
      <div className="login-page" style={{
         backgroundImage: `url(${bgImage})`,
         backgroundRepeat: "no-repeat",
         backgroundSize: "60% auto",
         backgroundPosition: "right 50% top 40%"
      }}>
         <section className="login-page__header">
            <h1>Kabu <span id="login-page__shop">Shop</span></h1>
            <p>Already a member? <a href="/" id="login-page__sign-in-link">sign in</a></p>
         </section>
         <h2 className="center">Create an account</h2>
         <section className="login-page__body">

            <form onSubmit={handleOnSubmit} className="login-page__form">
               <div className="login-page__form-names">
                  <input type="text" name="firstName" id="firstName" placeholder="First Name" value={loginFormData.firstName} onChange={handleOnChange} className="login-page__form-input" />
                  <input type="text" name="lastName" id="lastName" placeholder="Last Name" value={loginFormData.lastName} onChange={handleOnChange} className="login-page__form-input" />
               </div>
               <input type="email" name="email" id="email" placeholder="Email" value={loginFormData.email} onChange={handleOnChange} className="login-page__form-input" />
               <input type="password" name="password" id="password" placeholder="Password" value={loginFormData.password} onChange={handleOnChange} className="login-page__form-input" />

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
               <div className="login-page__oauth-google"><i class="fa-brands fa-google text-primary"></i>{" "}Continue with Google</div>
            </div>
         </section>
         <div className="login-page__circle"></div>
      </div>
   )
}

export default Login;