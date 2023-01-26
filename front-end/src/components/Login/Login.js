import React from "react";
import bgImage from "../../assets/login-page-bg.png";
import "./login.css";

const Login = () => {
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

            <form className="login-page__form">
               <div className="login-page__form-names">
                  <input type="text" name="firstName" id="firstName" placeholder="First Name" className="login-page__form-input" />
                  <input type="text" name="lastName" id="lastName" placeholder="Last Name" className="login-page__form-input" />
               </div>
               <input type="email" name="email" id="email" placeholder="Email" className="login-page__form-input" />
               <input type="password" name="password" id="password" placeholder="Password" className="login-page__form-input" />

               <p className="login-page__policy">
                  By Creating an account, you agree to our <span className="login-page__user-agreement">User Agreement- opens in new window
                     or tab</span> and acknowledge reading our <span className="login-page__user-agreement">User Privacy Notice- opens in new window or tab</span>.
               </p>
               <div className="login-page__btn-div">
               <button className="login-page__button">Create Account</button>
               </div>
            </form>
            <div className="or">
            <span className="login-page__or">or</span>
            </div>
            <div className="login-page__oauth">
               <div className="m-0 login-page__oauth-facebook"><i class="fa-brands fa-facebook"></i>{" "}Continue with Facebook</div>
               <div className="login-page__oauth-apple"><i class="fa-brands fa-apple"></i>{" "}Continue with Apple</div>
            </div>
         </section>
         <div className="login-page__circle"></div>
      </div>
   )
}

export default Login;