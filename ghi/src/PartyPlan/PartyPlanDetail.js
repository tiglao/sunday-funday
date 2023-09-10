import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import { baseUrl } from "../utils/config.js";
import InvitationForm from "./InviteModal.js";
import { useAccountContext } from "../utils/AccountContext.js";
import { formatDateTime } from "../utils/dashboardDateTime.js";

const PartyPlanDetail = ({ parentPartyPlan }) => {
  const { id } = useParams();
  const { accountAvatar, accountFullName } = useAccountContext();
  const navigate = useNavigate();
  const [partyPlan, setPartyPlan] = useState(parentPartyPlan || null);
  const [invitations, setInvitations] = useState([]);
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [startDate, setStartDate] = useState("");
  const [, setEndDate] = useState("");
  const [, setDisplayTime] = useState("");
  const [showInviteModal, setShowInviteModal] = useState(false);

  const emailAllGuests = () => {
    const allEmails = invitations
      .map((invite) => invite.account.email)
      .join(",");
    window.location.href = `mailto:${allEmails}`;
  };
  const toggleInviteModal = () => setShowInviteModal(!showInviteModal);
  const openInviteModal = () => {
    setShowInviteModal(true);
  };
  useEffect(() => {
    const handleBrowserBackButton = (e) => {
      e.preventDefault();
      navigate("/dashboard");
    };

    window.addEventListener("popstate", handleBrowserBackButton);

    return () => {
      window.removeEventListener("popstate", handleBrowserBackButton);
    };
  }, []);

  useEffect(() => {
    const fetchPartyPlan = async () => {
      try {
        const response = await fetch(`${baseUrl}/party_plans/${id}`);

        if (response.ok) {
          const data = await response.json();
          setPartyPlan(data);

          const { startDate, startTime, endDate, endTime, displayTime } =
            formatDateTime(data.start_time, data.end_time);
          setStartTime(startTime);
          setEndTime(endTime);
          setStartDate(startDate);
          setEndDate(endDate);
          setDisplayTime(displayTime);
        } else {
          console.log("Response not okay. Status:", response.status);
        }
      } catch (error) {
        console.error("Error fetching specific plan:", error);
      }
    };

    if (id) {
      fetchPartyPlan();
    }
  }, [id]);

  useEffect(() => {
    const fetchInvitations = async () => {
      if (partyPlan && partyPlan.invitations.length > 0) {
        try {
          const response = await fetch(
            `${baseUrl}/invitations?ids=${partyPlan.invitations.join(",")}`
          );
          if (response.ok) {
            const data = await response.json();
            setInvitations(data);
          } else {
            console.log("Response not okay. Status:", response.status);
          }
        } catch (error) {
          console.error("Error fetching invitations:", error);
        }
      }
    };

    fetchInvitations();
  }, [partyPlan]);

  if (!partyPlan) {
    return (
      <div className="container party-plan-detail">
        <h1>Loading...</h1> {/* Or any other placeholder */}
      </div>
    );
  }

  return (
    <div className="container party-plan-detail">
      {/* First Row */}
      <div className="row">
        <div className="col-md-5">
          {/* Party Image */}
          <img
            src={partyPlan.image}
            alt={partyPlan.description}
            className="img-fluid party-image"
          />
        </div>
        <div className="col-md-7 align-self-end">
          {/* Basic Info */}
          <div className="row">
            <div className="col start-date">{startDate}</div>
          </div>
          <div className="row mb-4">
            <div className="col display-time">
              {startTime} - {endTime}
            </div>
          </div>{" "}
          {/* party planner */}
          <div className="planner-description d-flex flex-column align-items-start">
            <div className="account-avatar">
              <img
                src={
                  accountAvatar
                    ? accountAvatar
                    : "https://i.pinimg.com/originals/fa/80/ed/fa80ed839cd94404434407f892a736cc.jpg"
                }
                alt="planner-avatar"
                className="account-avatar-crop"
              />
            </div>
            <div className="planner-name">Planned by: {accountFullName}</div>
          </div>
        </div>
      </div>

      {/* Second Row */}
      <div className="row mt-4">
        <div className="col-md-6">
          {/* Description and Keywords */}
          <div className="keywords">{partyPlan.keywords.join(", ")}</div>
          <div className="description mb-3">{partyPlan.description}</div>
        </div>

        <div className="col-md-6">
          {/* Invitations */}
          <div className="d-flex flex-wrap justify-content-start">
            {invitations.map((invite, index) => (
              <div key={invite.id} className="m-2 invite-card-container">
                <div className="invite-card">
                  <div className="invite-card-image-wrapper">
                    <img
                      src={
                        invite.account.avatar || "https://picsum.photos/140/80"
                      }
                      alt={`${invite.account.fullname}'s avatar`}
                      className="invite-card-image"
                    />
                  </div>
                  <div className="invite-card-content">
                    <small className="invite-card-text font-monospace">
                      <a
                        href={`mailto:${invite.account.email}`}
                        className="invite-card-link"
                      >
                        {invite.account.fullname}
                      </a>
                    </small>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div>
            <Button variant="primary" onClick={openInviteModal}>
              invite someone
            </Button>
            <Button variant="secondary" onClick={emailAllGuests}>
              email all
            </Button>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-md-5">
          <Button variant="secondary" onClick={() => navigate(-1)}>
            Go Back
          </Button>
        </div>
        <div className="col-md-7 align-self-end"></div>
      </div>

      <InvitationForm show={showInviteModal} onHide={toggleInviteModal} />
    </div>
  );
};

export default PartyPlanDetail;
