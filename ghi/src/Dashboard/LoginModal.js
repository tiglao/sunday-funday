import { useState, useEffect } from "react";
import { useRef } from "react";
import { Modal, Button, Spinner } from "react-bootstrap";
import { NavLink, useNavigate } from "react-router-dom";
import useToken from "@galvanize-inc/jwtdown-for-react";
import SignupForm from "../Auth/SignupForm";

const LoginModal = () => {
  const [show, setShow] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isError, setIsError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { login, token } = useToken();
  const navigate = useNavigate();

  const showRef = useRef(show);

  const handleClose = () => {
    setUsername("");
    setPassword("");
    setShow(false);
    showRef.current = false;
  };

  const handleShow = () => {
    setShow(true);
    showRef.current = true;
  };

  useEffect(() => {
    if (token !== null && showRef.current) {
      setIsError(false);
      navigate("/dashboard");
      handleClose();
    }
  }, [token, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    await login(username, password);

    setTimeout(() => {
      setIsLoading(false);
      if (token === null) {
        setIsError(true);
        setErrorMessage(
          "Oops! The email or password you entered is incorrect. 🙈"
        );
        setPassword("");
      } else {
        setUsername("");
        setPassword("");
      }
    }, 500);
  };

  let errorClass = "alert alert-danger d-none";

  if (isError) {
    errorClass = "alert alert-danger";
  }

  const handleInputChange = (e, setter) => {
    setIsError(false);
    setter(e.target.value);
  };

  const handlePasswordToggle = () => {
    setShowPassword(!showPassword);
  };

  return (
    <>
      {!token && (
        <li className="nav-item">
          <NavLink className="nav-link text-white" onClick={handleShow}>
            Login
          </NavLink>
        </li>
      )}
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Login</Modal.Title>
        </Modal.Header>
        <Modal.Body className="">
          <form onSubmit={(e) => handleSubmit(e)}>
            <div className="mb-3">
              <label className="form-label">Username</label>
              <input
                name="username"
                value={username}
                type="text"
                className="form-control"
                onChange={(e) => handleInputChange(e, setUsername)}
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Password</label>
              <div className="input-group">
                <input
                  name="password"
                  value={password}
                  type={showPassword ? "text" : "password"}
                  className="form-control"
                  onChange={(e) => handleInputChange(e, setPassword)}
                />
                <button
                  className="btn btn-outline-secondary"
                  type="button"
                  onClick={handlePasswordToggle}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>
            <Modal.Footer>
              {isLoading ? (
                <Spinner animation="border" role="status">
                  <span className="visually-hidden">Loading...</span>
                </Spinner>
              ) : (
                <div className={errorClass}>{errorMessage}</div>
              )}
              <Button variant="danger" onClick={handleClose}>
                Cancel
              </Button>
              <Button variant="primary" type="submit" value="Login">
                Login
              </Button>
            </Modal.Footer>
          </form>
          <div>
            {" "}
            {/* Bootstrap class to set text color to black */}
            <ul className="list-unstyled">
              {" "}
              {/* Bootstrap class to remove list item dot */}
              <SignupForm />
            </ul>
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default LoginModal;
