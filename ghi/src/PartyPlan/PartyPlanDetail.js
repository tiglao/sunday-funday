import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import React, { useEffect, useState } from "react";
import { FaEdit, FaCheck } from "react-icons/fa";
import Button from "react-bootstrap/Button";
import { baseUrl } from "../utils/config.js";
import { useDashboard } from "../utils/DashboardContext";
import InvitationForm from "./InviteModal.js";
import { useAccountContext } from "../utils/AccountContext.js";
import { useNavigate, Outlet } from "react-router-dom";
import { formatDateTime } from "../utils/dashboardDateTime.js";

const PartyPlanDetail = ({ parentPartyPlan }) => {
  const { accountAvatar, accountFullName } = useAccountContext();
  const { selectedPartyPlanId } = useDashboard();
  const navigate = useNavigate();
  const { token } = useAuthContext();
  const [partyPlan, setPartyPlan] = useState(parentPartyPlan || null);
  const [invitations, setInvitations] = useState([]);
  const [isEditing, setIsEditing] = useState(null);
  const [updatedValue, setUpdatedValue] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [displayTime, setDisplayTime] = useState("");
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
    const fetchPartyPlan = async () => {
      try {
        const response = await fetch(
          `${baseUrl}/party_plans/${selectedPartyPlanId}`
        );
        if (response.ok) {
          const data = await response.json();
          setPartyPlan({
            ...data,
            type: "partyPlan",
          });
          const { startDate, startTime, endDate, endTime, displayTime } =
            formatDateTime(data.start_time, data.end_time);
          console.log("Formatted Start Date:", startDate);
          console.log("Formatted Start Time:", startTime);
          console.log("Formatted End Date:", endDate);
          console.log("Formatted End Time:", endTime);
          console.log("Formatted Display Time:", displayTime);
          console.log("Fetched specific party plan:", data);
          setStartTime(startTime);
          setEndTime(endTime);
          setStartDate(startDate);
          setEndDate(endDate);
          setEndDate(displayTime);
        }
      } catch (error) {
        console.error("Error fetching specific plan:", error);
      }
    };

    if (selectedPartyPlanId) {
      fetchPartyPlan();
    }
  }, [selectedPartyPlanId]);

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
          }
        } catch (error) {
          console.error("Error fetching invitations:", error);
        }
      }
    };

    fetchInvitations();
  }, [partyPlan]);

  const handleEditClick = (field) => {
    setIsEditing(field);
    setUpdatedValue(partyPlan[field]);
  };

  const handleCheckClick = async (field) => {
    // TODO: Update the backend with the new value
    setIsEditing(null);
    setUpdatedValue("");
  };

  const renderEditableField = (field, value) => {
    if (isEditing === field) {
      return (
        <div>
          <input
            type="text"
            value={updatedValue}
            onChange={(e) => setUpdatedValue(e.target.value)}
          />
          <FaCheck className="icon" onClick={() => handleCheckClick(field)} />
        </div>
      );
    }
    return (
      <div className="editable-field">
        {value}
        <FaEdit className="icon" onClick={() => handleEditClick(field)} />
      </div>
    );
  };

  if (!partyPlan) {
    return <div>Loading...</div>;
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
              email ail
            </Button>
          </div>
        </div>
      </div>

      <InvitationForm show={showInviteModal} onHide={toggleInviteModal} />
    </div>
  );
};

export default PartyPlanDetail;
