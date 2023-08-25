import React, { useState } from "react";
import Button from "react-bootstrap/Button";
import { Modal } from "react-bootstrap";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";

function Nav() {
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  const handleLoginClose = () => setShowLogin(false);
  const handleLoginShow = () => setShowLogin(true);

  const handleSignupClose = () => setShowSignup(false);
  const handleSignupShow = () => setShowSignup(true);

  const handleSignupFromLogin = () => {
    handleLoginClose();
    handleSignupShow();
  };

  return (
    <div className="d-flex align-items-center justify-content-center mt-5 pt-5">
      <div className="text-center w-50 bg-dark bg-opacity-50 rounded-3 p-4">
        <h1>The greatest party planning app on earth</h1>
        <div className="d-flex justify-content-around mx-auto">
          <Button
            onClick={handleLoginShow}
            className="btn main-buttons text-white m-3 px-5"
          >
            Login
          </Button>

          <Button
            onClick={handleSignupShow}
            className="btn main-buttons text-white m-3 px-5"
          >
            Signup
          </Button>
        </div>

        <Modal show={showLogin} onHide={handleLoginClose}>
          <LoginForm
            handleSignupFromLogin={handleSignupFromLogin}
            handleLoginClose={handleLoginClose}
          />
        </Modal>
        <Modal show={showSignup} onHide={handleSignupClose}>
          <SignupForm handleSignupClose={handleSignupClose} />
        </Modal>
      </div>
    </div>
  );
}

export default Nav;
