import { useState, useEffect } from "react";
import { useRef } from "react";
import { Modal, Button, Spinner } from "react-bootstrap";
import { NavLink, useNavigate } from "react-router-dom";
import useToken from "@galvanize-inc/jwtdown-for-react";

const SignupForm = ({ handleSignupClose }) => {
  const [full_name, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  // const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const { register, token } = useToken();
  const navigate = useNavigate();

  const react_url = process.env.REACT_APP_API_HOST;

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

    setTimeout(() => {
      setIsLoading(false);
      if (token === null) {
        setIsError(true);
        setErrorMessage(
          "Oops! That email has already been used. Please use a different email or log in. 🙈"
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

  const handleInputChange = (e, setter) => {
    setIsError(false);
    setter(e.target.value);
  };

  useEffect(() => {
    if (token !== null) {
      handleSignupClose();
      navigate("/dashboard");
    }
  }, [token, navigate, handleSignupClose]);

  return (
    <>
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
              required
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
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Password</label>
            <div className="input-group">
              <input
                name="password"
                value={password}
                type="password"
                className="form-control"
                onChange={(e) => handleInputChange(e, setPassword)}
                required
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
            <Button variant="danger" onClick={handleSignupClose}>
              Cancel
            </Button>
            <Button variant="primary" type="submit" value="Login">
              Sign Up
            </Button>
          </Modal.Footer>
        </form>
      </Modal.Body>
    </>
  );
};

export default SignupForm;
