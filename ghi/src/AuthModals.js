import React, { useState } from "react";
import LoginModal from "./LoginModal";
import SignupForm from "./SignupForm";

const AuthModals = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  const handleShowLogin = () => {
    setShowLogin(true);
    setShowSignup(false);
  };

  const handleShowSignup = () => {
    setShowLogin(false);
    setShowSignup(true);
  };

  return (
    <>
      <LoginModal
        show={showLogin}
        onClose={() => setShowLogin(false)}
        onShowSignup={handleShowSignup}
      />
      <SignupForm show={showSignup} onClose={() => setShowSignup(false)} />
      <button onClick={handleShowLogin}>Open Login</button>{" "}
      {/* Example button to open login modal */}
    </>
  );
};

export default AuthModals;
