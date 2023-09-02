import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useNavigate, Link } from "react-router-dom";
import Button from "react-bootstrap/Button";
import React, { useState, useEffect } from "react";
import { baseUrl } from "./common/config.js";
import FeedbackModal from "./FeedbackModal";
import SideNav from "./SideNav";

function Dashboard() {
  const { token } = useAuthContext();
  const navigate = useNavigate();
  const [feedbackModalVisible, setFeedbackModalVisible] = useState(false);

  return (
    <>
      <div className="bg-dark shadow">
        {/* ... (other elements) ... */}
        <FeedbackModal
          show={feedbackModalVisible}
          handleClose={() => setFeedbackModalVisible(false)}
        />
      </div>
      <Button
        onClick={() => setFeedbackModalVisible(true)}
        style={{
          position: "fixed",
          bottom: "20px",
          right: "20px",
          zIndex: 1000,
        }}
      >
        Feedback
      </Button>
      <div className="bg-dark shadow">
        <div className="container-xxl p-0 bg-white min-vh-100">
          {/* Header */}
          <div className="curved-header text-center text-white">
            <h1 className="header-text p-3">Sunday Funday</h1>
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

            {/* What is this */}
            <div className="circle d-flex align-items-center justify-content-center">
              <a
                className="btn circle-button white-color d-lg-none"
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
                </svg>
              </a>
            </div>
          </div>

          {/* What is this */}
          <div
            className="offcanvas offcanvas-start slide-nav"
            tabIndex="-1"
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

          {/* Main Content */}
          <div className="row mx-5 mt-5">
            {/* Side Nav */}
            <div className="col-2 border main-nav rounded-3 text-end p-3 d-none d-lg-block">
              <SideNav />
            </div>
            {/* Main Content Area */}
            <div className="col-md-10 col-12 p-0 border">
              Hello world, I am main content.!!
            </div>
          </div>
          {/* Footer */}
          <div className="footer border">Footer</div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;
