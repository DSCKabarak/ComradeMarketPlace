import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import bgImage from "../../assets/login-page-bg.png";
import "./login.css";
import Modal from 'react-bootstrap/Modal';
import {
   Form,
   FormGroup,
   Input,
} from "reactstrap";

const Login = () => {

   const navigate = useNavigate();

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


   const [formErrors, setFormErrors] = useState({
      first_name: "",
      last_name: "",
      email: "",
      password: ""
   })

   const [isInputValid, setIsInputValid] = useState({
      first_name: false,
      last_name: false,
      email: false,
      password: false
   })

   const [show, setShow] = useState(false);

   const [error, setError] = useState("");

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
         .then(res => {
            if (!res.ok) {
               setError("Invalid username/password")
               throw new Error("Error authenticating")
            }
            return res.json()
         })
         .then((data) => {
            sessionStorage.setItem('user', JSON.stringify(data))
            navigate("/")
         })
         .catch(err => {
            console.log("Error ", err)
            sessionStorage.setItem('user', null)
            navigate("/login")
         })
   }

   function handleOnBlur(e) {
      if (registerFormData.first_name.length <= 3) {
         setFormErrors((prevFormErr) => ({
            ...prevFormErr,
            [e.target.id]: "First name should be greater than 3 characters"
         }))
      }
      else if (registerFormData.first_name.length >= 10) {
         setFormErrors((prevFormErr) => ({
            ...prevFormErr,
            [e.target.id]: "First name should be less than 10 characters"
         }))
      } else {
         setFormErrors((prevFormErr) => ({
            ...prevFormErr,
            [e.target.id]: ""
         }))
         setIsInputValid((prevFormErr) => ({
            ...prevFormErr,
            [e.target.id]: true
         }))
      }
      if ((/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(registerFormData.email))) {
         setFormErrors((prevFormErr) => ({
            ...prevFormErr,
            email: ""
         }))
         setIsInputValid((prevFormErr) => ({
            ...prevFormErr,
            email: true
         }))
      } else {
         setFormErrors((prevFormErr) => ({
            ...prevFormErr,
            email: "Email should be strong"
         }))
      }
      if (/^(?=.*\d)(?=.*[a-zA-Z])(?!.*\s).{1,15}$/i.test(registerFormData.password)) {
         setFormErrors((prevFormErr) => ({
            ...prevFormErr,
            [e.target.id]: ""
         }))
         setIsInputValid((prevFormErr) => ({
            ...prevFormErr,
            [e.target.id]: true
         }))
      } else {
         setFormErrors((prevFormErr) => ({
            ...prevFormErr,
            [e.target.id]: "Password must be strong"
         }))
      }
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
         .then(res => {
            if (!res.ok) {
               setError("Email is already registered please login")
               throw new Error("Error registering")
            }
            return res.json()
         })
         .then(data => {
            console.log(data)
         })
         .catch(err => console.log("Err", err))
   }

   return (
      <>
         {/* <Form>
        <FormGroup>
          <Label for="exampleEmail">Input without validation</Label>
          <Input />
          <FormFeedback>can't see this</FormFeedback>
          <FormText>some text.</FormText>
        </FormGroup>
        <FormGroup>
          <Label>Valid input</Label>
          <Input valid={false} invalid={true} />
          <FormFeedback valid={false} invalid={true}>looks good</FormFeedback>
          <FormText>some text.</FormText>
        </FormGroup>
        <FormGroup>
          <Label>Invalid input</Label>
          <Input invalid />
          <FormFeedback>invalid input</FormFeedback>
          <FormText>some text.</FormText>
        </FormGroup>
        <FormGroup>
          <Label>Input without validation</Label>
          <Input />
          <FormFeedback tooltip>looks good</FormFeedback>
          <FormText>some text.</FormText>
        </FormGroup>
        <FormGroup>
          <Label>Valid input</Label>
          <Input valid={false} />
          <FormFeedback tooltip>
            looks good
          </FormFeedback>
          <FormText>some text.</FormText>
        </FormGroup>
        <FormGroup>
          <Label>Invalid input</Label>
          <Input invalid />
          <FormFeedback tooltip>invalid input</FormFeedback>
          <FormText>some text.</FormText>
        </FormGroup>
      </Form>
     */}
         {error &&
            <div class="alert alert-danger d-flex align-items-center position-absolute w-100 d-flex justify-content-between opacity-40" role="alert">
               <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlinkHref="#exclamation-triangle-fill" /></svg>
               <div>
                  {error}
               </div>
               <button type="button" class="btn-close" onClick={() => window.location.reload()} data-bs-dismiss="alert" aria-label="Close"></button>
            </div>}
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
            backgroundPosition: "right 50% top 40%",
            minHeight: "100vh",
         }}>
            <section className="login-page__header">

               <h1>Kabu <span id="login-page__shop">Shop</span></h1>
               <p><span className="d-none d-md-inline">Already a member? </span> <span id="login-page__sign-in-link" onClick={handleShow} >sign in</span></p>
            </section >
            <h2 className="center">Create an account</h2>
            <section className="login-page__body">

               <Form onSubmit={handleOnSubmit} className="login-page__form">
                  <FormGroup className="login-page__form-names w-90">
                     <Input type="text" name="first_name" id="first_name" placeholder="First Name" value={registerFormData.first_name} onChange={handleOnChange} onBlur={handleOnBlur} className="mb-3 mb-md-6 login-page__form-input" valid={isInputValid.first_name} invalid={formErrors.first_name ? true : false} />
                     <Input type="text" name="last_name" id="last_name" placeholder="Last Name" value={registerFormData.last_name} onChange={handleOnChange} onBlur={handleOnBlur} className="mb-3 mb-md-6 d-block login-page__form-input" valid={isInputValid.last_name} invalid={formErrors.last_name ? true : false} />
                  </FormGroup>
                  <FormGroup>
                     <Input type="email" name="email" id="email" placeholder="Email" value={registerFormData.email} onChange={handleOnChange} className="mb-3 mb-md-6 login-page__form-input" onBlur={handleOnBlur} valid={isInputValid.email} invalid={formErrors.email ? true : false} />
                  </FormGroup>
                  <FormGroup>
                     <Input type="password" name="password" id="password" placeholder="Password" value={registerFormData.password} onChange={handleOnChange} onBlur={handleOnBlur} valid={isInputValid.password} invalid={formErrors.password ? true : false} className="mb-3 mb-md-6 login-page__form-input" />
                  </FormGroup>
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
               </Form>
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