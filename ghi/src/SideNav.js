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
    logout();
    handleLoginClose();
    handleSignupClose();
  };

  return (
    <div className="d-flex justify-content-end ">
      <nav className="">
        <ul className="navbar-nav flex-column">
          {token ? (
            <>
              <li className="nav-item">
                <NavLink className="nav-link text-dark" to="/dashboard">
                  Dashboard
                </NavLink>
                <NavLink className="nav-link text-dark" to="/invitee">
                  Invitee Dashboard
                </NavLink>
                <NavLink
                  className="nav-link text-dark"
                  onClick={handleLogout}
                  to="/"
                >
                  Logout
                </NavLink>
              </li>
            </>
          ) : (
            <>
              <li className="nav-item">
                <NavLink
                  onClick={handleLoginShow}
                  className="text-decoration-none text-dark"
                >
                  Login
                </NavLink>
                <NavLink
                  onClick={handleSignupShow}
                  className="text-decoration-none text-dark"
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
              </li>
            </>
          )}
        </ul>
      </nav>
    </div>
  );
}
export default Nav;
