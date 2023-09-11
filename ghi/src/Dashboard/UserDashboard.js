import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import { FaArrowUp } from "react-icons/fa";
import { baseUrl } from "../utils/config.js";
import { formatDateTime } from "../utils/dashboardDateTime.js";
import { PartyPlanForm } from "../PartyPlan/PartyPlanModal.js";
import { useAccountContext } from "../utils/AccountContext.js";

function UserDashboard() {
  const { accountEmail, accountId } = useAccountContext();
  const [, setSelectedLink] = useState("parties");
  const [partyPlans, setPartyPlans] = useState([]);
  const [invitations, setInvitations] = useState([]);
  const [currentData, setCurrentData] = useState([]);
  const [waitingPartyPlanData, setWaitingPartyPlanData] = useState(null);
  const [showPartyPlanForm, setShowPartyPlanForm] = useState(false);

  // nav
  const navigate = useNavigate();

  const handleComingUpArrow = (id) => {
    if (id === undefined) {
      console.log("ID is undefined. Something is wrong.");
      return;
    }

    navigate(`/dashboard/party_plans/${id}`);
  };

  const handleWaitingArrow = (id) => {
    const selectedWaitingPartyPlan = partyPlans.find((plan) => plan.id === id);
    if (selectedWaitingPartyPlan) {
      setWaitingPartyPlanData(selectedWaitingPartyPlan);
    }
    setShowPartyPlanForm(true);
  };

  // event handlers

  const togglePartyPlanForm = () => setShowPartyPlanForm(!showPartyPlanForm);
  const openPartyPlanForm = () => {
    setShowPartyPlanForm(true);
  };
  const closePartyPlanForm = () => {
    setShowPartyPlanForm(false);
  };

  const refreshDashboard = async () => {
    await fetchPlans();
    closePartyPlanForm();
  };

  const fetchInvitations = useCallback(async () => {
    try {
      const response = await fetch(`${baseUrl}/invitations/`);
      if (response.ok) {
        const data = await response.json();
        const compiledInvitations = data
          .filter((invite) => invite.account.email === accountEmail)
          .map((invite) => ({
            ...invite,
            type: "invitation",
          }));
        setInvitations(compiledInvitations);
      }
    } catch (error) {
      console.error("Error fetching invitations:", error);
    }
  }, [accountEmail]);

  const fetchPlans = useCallback(async () => {
    try {
      const response = await fetch(`${baseUrl}/party_plans/`);
      if (response.ok) {
        const data = await response.json();
        const compiledPlans = data
          .filter((plan) => plan.account_id === accountId)
          .map((partyPlan) => ({
            ...partyPlan,
            type: "partyPlan",
          }));
        setPartyPlans(compiledPlans);
      }
    } catch (error) {
      console.error("Error fetching invitations:", error);
    }
  }, [accountId]);

  useEffect(() => {
    const fetchData = async () => {
      await fetchPlans();
      await fetchInvitations();
    };

    fetchData();
  }, [fetchPlans, fetchInvitations]);

  useEffect(() => {
    setCurrentData([...partyPlans, ...invitations]);
  }, [partyPlans, invitations]);

  //render functions
  const renderComingUp = () => {
    if (currentData) {
      return currentData.map((item, index) => {
        let startTime, endTime, imageUrl;

        if (item.type === "partyPlan") {
          startTime = item.start_time;
          endTime = item.end_time;
          imageUrl = item.image;
        } else if (item.type === "invitation") {
          const asscPartyPlan = partyPlans.find(
            (plan) => plan.id === item.party_plan_id
          );
          if (asscPartyPlan) {
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
          >
            <div className="card coming-up-card rounded">
              <div
                className="coming-up-image rounded"
                style={{ backgroundImage: `url(${imageUrl})` }}
              ></div>

              <div className="card-body">
                <div
                  className="coming-up-arrow"
                  onClick={() => {
                    handleComingUpArrow(item.id);
                  }}
                >
                  <FaArrowUp style={{ transform: "rotate(45deg)" }} />
                </div>

                <p className="card-text coming-up-text">
                  <span className="one-line">{startDate.toLowerCase()}</span>
                </p>
              </div>
            </div>

            <div className="description-under-card">
              <span>
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
                parties
              </Button>
              <Button
                variant="link"
                className="text-decoration-none no-outline me-5"
                onClick={() => {
                  setCurrentData(invitations);
                  setSelectedLink("invites");
                }}
              >
                invites
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
