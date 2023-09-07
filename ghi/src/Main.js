import MainLogin from "./MainLogin";
import { useEffect } from "react";
import useToken from "@galvanize-inc/jwtdown-for-react";
import { useNavigate, useLocation } from "react-router-dom";

function Main() {
  const { token } = useToken();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (token && location.pathname !== "/dashboard") {
      navigate("/dashboard");
    }
  }, [token, location, navigate]);

  return (
    <div className="bg-dark shadow">
      <div className=" container-xxl p-0 bg-disco min-vh-100">
        <div className="curved-header text-center text-white border-bottom border-3 border-white">
          <h1 className="header-text p-3">sunday funday</h1>
        </div>
        <div className="min-vh-100">
          <MainLogin />
        </div>
      </div>
    </div>
  );
}

export default Main;
