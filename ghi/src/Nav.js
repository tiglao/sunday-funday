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
  const { logout } = useToken();

  const handleLogout = () => {
    logout(); // Call the logout function from useToken
    handleLoginClose(); // Close the login modal
    handleSignupClose(); // Close the signup modal
  };

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
          <ul className="navbar-nav d-flex text-white">
            {token && (
              <>
                <li className="nav-item">
                  <NavLink className="nav-link text-white" to="/dashboard">
                    Dashboard
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link text-white" to="/invitee">
                    Invitee Dashboard
                  </NavLink>
                </li>
              </>
            )}
          </ul>
          <ul className="navbar-nav ms-auto">
            {!token && (
              <>
                <NavLink
                  onClick={handleLoginShow}
                  className="text-white text-decoration-none px-2"
                >
                  Login
                </NavLink>
                <NavLink
                  onClick={handleSignupShow}
                  className="text-white text-decoration-none px-2"
                >
                  Signup
                </NavLink>

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
            {token && (
              <NavLink
                className="nav-link text-white ms-auto"
                onClick={handleLogout} // Call the new handleLogout function here
                to="/"
              >
                Logout
              </NavLink>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Nav;
