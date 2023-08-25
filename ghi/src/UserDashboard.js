import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import SideNav from "./SideNav";

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
    <div className=" container-xxl p-0">
      <div className="curved-header text-center text-white">
        <h1 className="header-text p-3">sunday funday</h1>
        <form className="d-flex justify-content-center" role="search">
          <input
            className="form-control me-2 w-25 mb-5"
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
          <button className="btn btn-outline-success mb-5" type="submit">
            Search
          </button>
        </form>
      </div>
      <div className="row mx-5">
        <div className="col-2 border side-nav rounded-3 text-end p-3">
          <SideNav />
        </div>
        <div className="col-5 border mx-5">Coming up</div>
        <div className="col-4  border">waiting on you</div>
      </div>
    </div>
  );
}

export default UserDashboard;
