import { NavLink } from "react-router-dom";

function Nav() {
  return (
    <nav className="navbar navbar-expand-lg bg-dark border-bottom border-bod">
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
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav d-flex text-white">
            <li className="nav-item">
              <NavLink
                className="nav-link active text-white"
                aria-current="page"
                to="/login"
              >
                login
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link text-white" to="#">
                Logout
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link text-white" to="#">
                Link
              </NavLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Nav;
