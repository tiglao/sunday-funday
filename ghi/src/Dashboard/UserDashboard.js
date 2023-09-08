// import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
// import { useNavigate } from "react-router-dom";
import React, { useState, useEffect } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { Button, Modal } from "react-bootstrap";
import { FaArrowUp } from "react-icons/fa";
import { baseUrl } from "../utils/config.js";
import { formatDateTime } from "../utils/dashboardDateTime.js";
import { useDashboard } from "../utils/DashboardContext.js";
import { PartyPlanForm } from "../PartyPlanModal.js";
import {
  fetchData,
  dummyPartyPlans,
  dummyInvitations,
  fetchResource,
} from "../utils/dataService.js";
import { useAccountContext } from "../utils/AccountContext.js";

function UserDashboard() {
  // const { token } = useAuthContext();
  // const navigate = useNavigate();
  const { accountEmail, accountId } = useAccountContext();
  const { currentView, setCurrentView, showPartyPlanDetail } = useDashboard();
  const [selectedLink, setSelectedLink] = useState("parties");
  const [partyPlans, setPartyPlans] = useState([]);
  const [invitations, setInvitations] = useState([]);
  const [currentData, setCurrentData] = useState([]);
  const [waitingPartyPlanData, setWaitingPartyPlanData] = useState(null);
  const [showPartyPlanForm, setShowPartyPlanForm] = useState(false);
  const [waitingModal, setWaitingModal] = useState(false);
  const [waitingPartyPlanId, setwaitingPartyPlanId] = useState(null);

  // nav
  const navigate = useNavigate();
  const location = useLocation();

  const handleComingUpArrow = (id) => {
    setCurrentView("partyPlanDetail");
    console.log("handleComingUpArrow triggered with ID:", id);
    if (id === undefined) {
      console.log("ID is undefined. Something is wrong.");
      return;
    }
    showPartyPlanDetail(id);
  };

  const handleWaitingArrow = (id) => {
    setwaitingPartyPlanId(id);
    setWaitingModal(true);
  };

  // event handlers

  const togglePartyPlanForm = () => setShowPartyPlanForm(!showPartyPlanForm);
  const openPartyPlanForm = () => {
    setShowPartyPlanForm(true);
  };
  const closePartyPlanForm = () => {
    setShowPartyPlanForm(false);
  };
  const closeWaitingModal = () => {
    setWaitingModal(false);
  };

  const refreshDashboard = async () => {
    await fetchPlans();
    closePartyPlanForm();
  };

  // delete
  const handleCloseModal = () => {
    setWaitingModal(false);
  };

  // effect hooks
  // do not use until it works
  // useEffect(() => {
  //   const loadAsyncData = async () => {
  //     const data = await fetchData(accountId, accountEmail);
  //     setCurrentData(data);
  //   };
  //   loadAsyncData();
  // }, [accountId, accountEmail]);

  // omission makes coming up cards invalid
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

  useEffect(() => {
    console.log("Dummy Party Plans:", dummyPartyPlans);
    console.log("Dummy Invitations:", dummyInvitations);

    setCurrentData([...partyPlans, ...invitations]);
  }, [partyPlans, invitations]);

  // data
  // delete after verify
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

  //render functions
  // delete after verify
  const renderComingUp = () => {
    if (currentData) {
      return currentData.map((item, index) => {
        let displayContent, partyPath, startTime, endTime, imageUrl;

        if (item.type === "partyPlan") {
          displayContent = item.description;
          partyPath = `/party_plans/${item.id}`;
          startTime = item.start_time;
          endTime = item.end_time;
          imageUrl = item.image;
        } else if (item.type === "invitation") {
          const asscPartyPlan = partyPlans.find(
            (plan) => plan.id === item.party_plan_id
          );
          if (asscPartyPlan) {
            displayContent = asscPartyPlan.description;
            partyPath = `/party_plans/${item.party_plan_id}`;
            startTime = asscPartyPlan.start_time;
            endTime = asscPartyPlan.end_time;
            imageUrl = asscPartyPlan.image;
          }
        }

        const { startDate, displayTime } = formatDateTime(startTime, endTime);

        return (
          <div
            className="col-lg-4 col-md-6 col-sm-12 coming-up-col"
            key={index}
            onClick={() => {
              console.log("Item ID before passing to handler:", item.id);
              handleComingUpArrow(item.id);
            }}
          >
            <div className="card coming-up-card rounded">
              <div
                className="coming-up-image rounded"
                style={{ backgroundImage: `url(${imageUrl})` }}
              ></div>
              <div className="card-body">
                <div
                  onClick={() => handleComingUpArrow(item.id)}
                  className="coming-up-arrow"
                >
                  <FaArrowUp style={{ transform: "rotate(45deg)" }} />
                </div>
                <p className="card-text coming-up-text">
                  <span className="one-line">{startDate.toLowerCase()}</span>
                </p>
              </div>
            </div>
            <div className="description-under-card">
              <span className="coming-up-time">
                {displayTime}
                <br />
              </span>
            </div>
          </div>
        );
      });
    }
    return null;
  };

  const renderWaiting = () => {
    const allWaiting = partyPlans.filter(
      (plan) =>
        plan.party_status === "draft" || plan.party_status === "share draft"
    );
    return allWaiting.map((item, index) => {
      const { startDate, displayTime } = formatDateTime(
        item.start_time,
        item.end_time
      );

      return (
        <div className="card waiting-cards p-3 mb-3 ml-4" key={index}>
          <div
            className="card-body"
            style={{ padding: "0", paddingTop: "2px" }}
          >
            <div
              className="waiting-arrow"
              onClick={() => handleWaitingArrow(item.id)}
            >
              <FaArrowUp style={{ transform: "rotate(45deg)" }} />
            </div>
            <p className="card-text one-line">
              {item.description}
              <br />
              <span className="waiting-date-time">
                {startDate.toLowerCase()} | {displayTime}
              </span>
            </p>
          </div>
        </div>
      );
    });
  };

  return (
    <>
      <div className="row">
        <div className="col-md-6">
          <div className="row mb-4">
            <div className="col-4">
              <h3>coming up</h3>
            </div>
            <div className="col-8 d-flex justify-content-start">
              <Button
                variant="link"
                className="text-decoration-none no-outline"
                onClick={() => {
                  setCurrentData(partyPlans);
                  setSelectedLink("parties");
                }}
              >
                my parties
              </Button>
              <Button
                variant="link"
                className="text-decoration-none no-outline ml-2"
                onClick={() => {
                  setCurrentData(invitations);
                  setSelectedLink("invites");
                }}
              >
                my invites
              </Button>
              <Button variant="secondary" onClick={openPartyPlanForm}>
                start a party
              </Button>
            </div>
          </div>
          <div className="d-flex flex-wrap justify-content-start">
            {renderComingUp()}
          </div>
        </div>
        <div className="col-md-6 pl-4 waiting-section">
          <h3 className="ps-2 section-title">waiting on you</h3>
          <div className="row ps-2 waiting-card">{renderWaiting()}</div>
        </div>
      </div>
      <Outlet />
      <PartyPlanForm
        show={showPartyPlanForm}
        onHide={togglePartyPlanForm}
        partyPlanData={waitingPartyPlanData}
        refreshDashboard={refreshDashboard}
      />
    </>
  );
}

export default UserDashboard;
