import { useState, useEffect } from "react";
import { useRef } from "react";
import { Modal, Button, Spinner } from "react-bootstrap";
import { NavLink, useNavigate } from "react-router-dom";
import useToken from "@galvanize-inc/jwtdown-for-react";

const SignupForm = () => {
  const [full_name, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [show, setShow] = useState(false);
  const { register, token } = useToken();
  //   const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const react_url = process.env.REACT_APP_API_HOST;

  const showRef = useRef(show);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userData = {
      username: email,
      password: password,
      email: email,
      full_name: full_name,
    };
    setIsLoading(true);
    register(userData, `${react_url}/api/accounts`);
    // e.target.reset();

    setTimeout(() => {
      setIsLoading(false);
      if (token === null) {
        setIsError(true);
        setErrorMessage(
          "Oops! The username or password you entered is incorrect. Please double-check and try again."
        );
        setPassword("");
      } else {
        setEmail("");
        setFullName("");
        setPassword("");
      }
    }, 500);
  };

  let errorClass = "alert alert-danger d-none";

  if (isError) {
    errorClass = "alert alert-danger";
  }

  const handleClose = () => {
    setEmail("");
    setFullName("");
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

  const handleInputChange = (e, setter) => {
    setIsError(false);
    setter(e.target.value);
  };

  return (
    <>
      {!token && (
        <li className="nav-item">
          <NavLink className="nav-link text-white" onClick={handleShow}>
            Sign Up
          </NavLink>
        </li>
      )}
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Sign Up</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form onSubmit={(e) => handleSubmit(e)}>
            <div className="mb-3">
              <label className="form-label">Full Name</label>
              <input
                name="Full Name"
                value={full_name}
                type="text"
                className="form-control"
                onChange={(e) => handleInputChange(e, setFullName)}
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                name="email"
                value={email}
                type="email"
                className="form-control"
                onChange={(e) => handleInputChange(e, setEmail)}
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Password</label>
              <div className="input-group">
                <input
                  name="password"
                  value={password}
                  className="form-control"
                  onChange={(e) => handleInputChange(e, setPassword)}
                />
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
                Sign Up
              </Button>
            </Modal.Footer>
          </form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default SignupForm;
