import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useNavigate, NavLink } from "react-router-dom";
import Button from "react-bootstrap/Button";
import React, { useState, useEffect } from "react";
import SideNav from "./SideNav";

const partyData = [
  { content: "Party 1" },
  { content: "Party 2" },
  { content: "Party 3" },
  { content: "Party 4" },
  { content: "Party 5" },
  { content: "Party 6" },
];

const inviteData = [
  { content: "Invites 1" },
  { content: "Invites 2" },
  { content: "Invites 3" },
  { content: "Invites 4" },
  { content: "Invites 5" },
  { content: "Invites 6" },
];

const waitingData = [
  { content: "Waiting 1" },
  { content: "Waiting 2" },
  { content: "Waiting 3" },
];

function UserDashboard() {
  const { token } = useAuthContext();
  const navigate = useNavigate();
  const [currentData, setCurrentData] = useState(partyData);
  const [selectedLink, setSelectedLink] = useState("parties");
  // const [partyData, setPartyData] = useState();
  // const [inviteData, setInviteData] = useState();
  // const [waitingData, setWaitingData] = useState();

  useEffect(() => {
    if (!token) {
      navigate("/");
    }
  }, [token, navigate]);

  if (!token) {
    return null;
  }

  return (
    <div className="bg-dark shadow">
      <div className="container-xxl p-0 bg-white min-vh-100">
        <div className="curved-header text-center text-white">
          <h1 className="header-text p-3">sunday funday</h1>
          <form className="d-flex justify-content-center" role="search">
            <input
              className="form-control me-2 w-25 mb-5 me-3"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            <button
              className="btn search-button mb-5 rounded-circle"
              style={{ width: "50px", height: "50px" }}
            ></button>
          </form>
          <div className="circle d-flex align-items-center justify-content-center">
            <a
              className="btn circle-button white-color"
              data-bs-toggle="offcanvas"
              href="#offcanvasExample"
              role="button"
              aria-controls="offcanvasExample"
            >
              <svg
                viewBox="0 0 100 80"
                width="40"
                height="40"
                className="white-fill"
              >
                <rect width="100" height="20"></rect>
                <rect y="30" width="100" height="20"></rect>
                <rect y="60" width="100" height="20"></rect>
              </svg>
            </a>
          </div>
        </div>
        <div
          className="offcanvas offcanvas-start slide-nav"
          tabindex="-1"
          id="offcanvasExample"
          aria-labelledby="offcanvasExampleLabel"
        >
          <div className="offcanvas-header">
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="offcanvas"
              aria-label="Close"
            ></button>
          </div>
          <div className="offcanvas-body">
            <SideNav />
          </div>
        </div>
        <div className="row mx-5 mt-5">
          <div className="col-2 border main-nav rounded-3 text-end p-3">
            <SideNav />
          </div>
          <div className="col-md-5 col-12">
            <div className="row">
              <div className="d-flex ">
                <h3>coming up</h3>
                <Button
                  variant="link"
                  className="text-decoration-none no-outline"
                  style={{
                    color: selectedLink === "parties" ? "black" : "grey",
                  }}
                  onClick={() => {
                    setCurrentData(partyData);
                    setSelectedLink("parties");
                  }}
                >
                  my parties
                </Button>
                <Button
                  variant="link"
                  className="text-decoration-none no-outline"
                  style={{
                    color: selectedLink === "invites" ? "black" : "grey",
                  }}
                  onClick={() => {
                    setCurrentData(inviteData);
                    setSelectedLink("invites");
                  }}
                >
                  my invites
                </Button>
              </div>
              <div className="d-flex flex-wrap justify-content-around">
                {currentData.map((item, index) => (
                  <div className="p-2" key={index}>
                    <div className="image-placeholders p-3 mt-3">
                      {item.content}
                    </div>
                    <p className="text-center">Some words</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="col-md-5 col-12">
            <h3 className="ps-2">waiting on you</h3>
            <div className="row ps-2">
              {waitingData.map((item, index) => (
                <div className="" key={index}>
                  <div
                    className="dark-orange-attention p-3 mb-3"
                    style={{ minHeight: "70px" }}
                  >
                    {item.content}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserDashboard;
