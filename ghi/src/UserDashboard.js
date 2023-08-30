import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useNavigate, Link } from "react-router-dom";
import Button from "react-bootstrap/Button";
import React, { useState, useEffect } from "react";
import { baseUrl } from "./common/config.js";
<<<<<<< HEAD
=======
import { baseUrl } from "./common/config.js";
>>>>>>> de238e2c545c043adde39ff22cb0435a968825da
import SideNav from "./SideNav";
import PartyPlanDetail from "./PartyPlanDetail";

function UserDashboard() {
  const { token } = useAuthContext();
  const navigate = useNavigate();
  const [selectedLink, setSelectedLink] = useState("parties");
  const [partyPlans, setPartyPlans] = useState([]);
  const [invitations, setInvitations] = useState([]);
  const [currentData, setCurrentData] = useState([]);
  const [waitingData, setWaitingData] = useState([]);

  const fetchInvitations = async () => {
    try {
      const response = await fetch(`${baseUrl}/invitations/`);
      if (response.ok) {
        const data = await response.json();
        const compiledInvitations = data.map((invite) => ({
          ...invite,
          type: "invitation",
        }));
        setInvitations(compiledInvitations);
      }
    } catch (error) {
      console.error("Error fetching invitations:", error);
    }
  };

  const fetchPlans = async () => {
    try {
      const response = await fetch(`${baseUrl}/party_plans/`);
      if (response.ok) {
        const data = await response.json();
        const compiledPlans = data.map((partyPlan) => ({
          ...partyPlan,
          type: "partyPlan",
        }));
        setPartyPlans(compiledPlans);
      }
    } catch (error) {
      console.error("Error fetching invitations:", error);
    }
  };
  const handleShowParties = () => {
    setCurrentData(partyPlans);
  };

  const handleShowInvitations = () => {
    setCurrentData(invitations);
  };

  useEffect(() => {
    const fetchData = async () => {
      await fetchPlans();
      await fetchInvitations();
    };

    fetchData();
  }, []);

  useEffect(() => {
    setCurrentData([...partyPlans, ...invitations]);
  }, [partyPlans, invitations]);

  const renderCurrentData = () => {
    if (currentData) {
      return currentData.map((item, index) => {
        let displayContent;
        let linkPath;
        if (item.type === "partyPlan") {
          displayContent = item.description;
          linkPath = `/dashboard/party_plan/${item.id}`;
        } else if (item.type === "invitation") {
          displayContent = item.party_plan_id;
          linkPath = `/dashboard/party_plan/${item.party_plan_id}`;

          const correspondingPartyPlan = partyPlans.find(
            (plan) => plan.id === item.party_plan_id
          );

          if (correspondingPartyPlan) {
            console.log("Corresponding Party Plan:", correspondingPartyPlan);
          } else {
            console.log("Party Plan not found for ID:", item.party_plan_id);
          }
        }

        return (
          <Link to={linkPath} key={index}>
            <div className="p-2" key={index}>
              <div className="image-placeholders p-3 mt-3">
                {displayContent}
              </div>
              <p className="text-center">{displayContent}</p>
            </div>
          </Link>
        );
      });
    }
    return null;
  };

  const renderDrafts = () => {
    const allDrafts = partyPlans.filter(
      (plan) =>
        plan.party_status === "draft" || plan.party_status === "share draft"
    );
    return allDrafts.map((item, index) => (
      <div className="" key={index}>
        <div
          className="dark-orange-attention p-3 mb-3"
          style={{ minHeight: "70px" }}
        >
          {item.description}
        </div>
      </div>
    ));
  };
  // useEffect(() => {
  //   fetchPlans();
  //   fetchInvitations();

  //   const fetchData = async () => {
  //     await fetchPlans();
  //     await fetchInvitations();
  //     setCurrentData([...partyPlans, ...invitations]);
  //   };

  //   fetchData();
  // }, []);

  // useEffect(() => {
  //   if (!token) {
  //     navigate("/");
  //   }
  // }, [token, navigate]);

  // if (!token) {
  //   return null;
  // }

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
<<<<<<< HEAD
=======
                <rect y="60" width="100" height="20"></rect>
>>>>>>> de238e2c545c043adde39ff22cb0435a968825da
              </svg>
            </a>
          </div>
        </div>
        <div
          className="offcanvas offcanvas-start slide-nav"
          tabIndex="-1"
<<<<<<< HEAD
=======
          tabIndex="-1"
>>>>>>> de238e2c545c043adde39ff22cb0435a968825da
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
          <div className="col-2 border main-nav rounded-3 text-end p-3 d-none d-lg-block">
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
                    setCurrentData(partyPlans);
<<<<<<< HEAD
=======
                    setCurrentData(partyPlans);
>>>>>>> de238e2c545c043adde39ff22cb0435a968825da
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
                    setCurrentData(invitations);
<<<<<<< HEAD
=======
                    setCurrentData(invitations);
>>>>>>> de238e2c545c043adde39ff22cb0435a968825da
                    setSelectedLink("invites");
                  }}
                >
                  my invites
                </Button>
              </div>
              <div className="d-flex flex-wrap justify-content-around">
                {renderCurrentData()}
<<<<<<< HEAD
=======
                {renderCurrentData()}
>>>>>>> de238e2c545c043adde39ff22cb0435a968825da
              </div>
            </div>
          </div>
          <div className="col-md-5 col-12">
            <h3 className="ps-2">waiting on you</h3>
            <div className="row ps-2">{renderDrafts()}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserDashboard;
