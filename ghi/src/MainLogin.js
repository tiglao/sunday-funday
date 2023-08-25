import React, { useState } from "react";
import { Modal } from "react-bootstrap";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";
import useToken from "@galvanize-inc/jwtdown-for-react";
import { NavLink } from "react-router-dom";

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
  const { token } = useToken();

  return (
    <nav className="navbar navbar-expand-lg bg-dark container-xxl">
      <div className="container-fluid">
        <NavLink className="navbar-brand text-white" to="/">
          Sunday Funday
        </NavLink>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
          style={{ color: "white" }}
        >
          <span className="navbar-toggler-icon navbar-toggler-icon-white"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="nav nav-pills nav-fill">
            {!token && (
              <>
                <li className="nav-item">
                  <button
                    onClick={handleLoginShow}
                    className="nav-link btn btn-link text-dark px-2"
                  >
                    Login
                  </button>
                </li>
                <li className="nav-item">
                  <button
                    onClick={handleSignupShow}
                    className="nav-link btn btn-link text-dark px-2"
                  >
                    Signup
                  </button>
                </li>

                <Modal show={showLogin} onHide={handleLoginClose}>
                  <LoginForm
                    handleSignupFromLogin={handleSignupFromLogin}
                    handleLoginClose={handleLoginClose}
                  />
                </Modal>
                <Modal show={showSignup} onHide={handleSignupClose}>
                  <SignupForm handleSignupClose={handleSignupClose} />
                </Modal>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Nav;
