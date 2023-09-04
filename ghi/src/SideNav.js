import React, { useState, useRef, useEffect } from "react";
import { Modal } from "react-bootstrap";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";
import useToken from "@galvanize-inc/jwtdown-for-react";
import { NavLink } from "react-router-dom";

function Nav() {
  // auth
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

  // ui
  const [circleTop, setCircleTop] = useState("100px");
  const loginRef = React.createRef();
  const signupRef = React.createRef();
  const dashboardRef = React.createRef();

  const handleHover = (ref) => {
    if (ref.current) {
      setCircleTop(`${ref.current.offsetTop}px`);
    }
  };

  return (
    <div className="d-flex">
      <div
        className="circle d-flex align-items-center justify-content-center position-absolute"
        style={{ top: circleTop }}
      ></div>
      <nav className="sidenav-container">
        <ul
          className="navbar-nav flex-column"
          style={{ marginTop: "100px", paddingLeft: "30px" }}
        >
          {token ? (
            <>
              <li className="nav-item">
                <NavLink
                  ref={dashboardRef}
                  className="text-decoration-none d-block"
                  to="/dashboard"
                  onMouseEnter={() => handleHover(dashboardRef)}
                >
                  Dashboard
                </NavLink>
              </li>
              <li className="nav-item logout">
                <NavLink
                  className="text-decoration-none logout-link"
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
                  ref={loginRef}
                  className="text-decoration-none d-block"
                  onMouseEnter={() => {
                    handleHover(loginRef);
                  }}
                  onClick={handleLoginShow}
                >
                  Login
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink
                  ref={signupRef}
                  className="text-decoration-none d-block"
                  onMouseEnter={() => {
                    handleHover(signupRef);
                  }}
                  onClick={handleSignupShow}
                >
                  Signup
                </NavLink>
              </li>
              <li>
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
