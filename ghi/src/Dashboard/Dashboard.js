import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import { FaCommentDots, FaArrowRight } from "react-icons/fa";
import SideNav from "../SideNav";
import FeedbackModal from "./FeedbackModal";
function Dashboard() {
  const [feedbackModalVisible, setFeedbackModalVisible] = useState(false);

  return (
    <>
      <div className="bg-dark shadow">
        <FeedbackModal
          show={feedbackModalVisible}
          handleClose={() => setFeedbackModalVisible(false)}
        />
      </div>

      {/* Header */}
      <div className="curved-header">
        <span className="header-app-text p-3">SUNDAY</span>{" "}
        <img src="/logo512.png" alt="Logo" className="header-logo" />
        <span className="header-app-text p-3 mb-5">FUNDAY</span>
        <form className="d-flex justify-content-center" role="search">
          <input
            className="form-control header-search me-2 w-25 mb-5 me-3"
            type="search"
            placeholder="keyword search"
            aria-label="search"
          />
          <button
            className="btn search-button mb-5 rounded-circle"
            style={{ width: "50px", height: "50px" }}
          >
            <FaArrowRight size="1.3em" />
          </button>
        </form>
      </div>

      {/* Central Container */}
      <div>
        <div className="center container-xxl p-0 min-vh-100 extra-bottom-space">
          <div className="row mx-5 mt-5">
            {/* Side Nav */}
            <div className="col-2 border main-nav rounded-3 text-end p-3 d-none d-lg-block">
              <SideNav />
            </div>
            {/* Main Content Area */}
            <div className="dashboard-main col-md-10 col-12 p-0 extra-bottom-space">
              <Outlet />
            </div>
          </div>
        </div>
      </div>
      {/* Footer */}
      <div className="footer-container">
        <div className="svg-button-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 150">
            <path
              fill="#6C1CAC"
              fillOpacity="1"
              d="M0,32L40,37.3C80,43,160,53,240,53.3C320,53,400,43,480,37.3C560,32,640,32,720,37.3C800,43,880,53,960,53.3C1040,53,1120,43,1200,37.3C1280,32,1360,32,1400,37.3L1440,43L1440,150L1400,150C1360,150,1280,150,1200,150C1120,150,1040,150,960,150C880,150,800,150,720,150C640,150,560,150,480,150C400,150,320,150,240,150C160,150,80,150,40,150L0,150Z"
            ></path>
            <text
              x="50%"
              y="75%"
              dominantBaseline="middle"
              textAnchor="middle"
              fill="white"
              style={{ fontSize: "18px" }}
            >
              <a
                href="https://gitlab.com/leahnp613/sunday-funday"
                target="_blank"
                rel="noopener noreferrer"
              >
                visit our gitlab project
              </a>
            </text>
          </svg>
        </div>
        <button
          onClick={() => setFeedbackModalVisible(true)}
          className="feedback-button"
        >
          <FaCommentDots size="2em" />
        </button>
      </div>
    </>
  );
}

export default Dashboard;
