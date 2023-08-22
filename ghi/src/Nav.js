import { NavLink } from "react-router-dom";
import LoginModal from "./LoginModal";
import SignupForm from "./SignupForm";
import useToken from "@galvanize-inc/jwtdown-for-react";

const Nav = () => {
  const { token } = useToken();
  const { logout } = useToken();
  return (
    <nav className="navbar navbar-expand-lg bg-dark">
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
            <LoginModal />
            <SignupForm />
            {token && (
              <li className="nav-item">
                <NavLink
                  className="nav-link text-white ms-auto"
                  onClick={logout}
                  to="/"
                >
                  Logout
                </NavLink>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Nav;
