import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

function UserDashboard() {
  const { token } = useAuthContext();
  const navigate = useNavigate();
  useEffect(() => {
    if (!token) {
      navigate("/");
    }
  }, [token, navigate]);

  if (!token) {
    return null;
  }

  return (
    <div className=" container-xxl ">
      <div className="curved-header text-center text-white">
        <h1 className="header-text p-4">sunday funday</h1>
      </div>
      <div className="">
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  );
}

export default UserDashboard;
