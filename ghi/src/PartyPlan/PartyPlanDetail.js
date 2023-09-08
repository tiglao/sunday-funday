import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import React, { useEffect, useState } from "react";
import { FaEdit, FaCheck } from "react-icons/fa";
import Button from "react-bootstrap/Button";
import { baseUrl } from "../utils/config.js";
import { useDashboard } from "../utils/DashboardContext";
import InvitationForm from "./InviteModal.js";
import { useAccountContext } from "../utils/AccountContext.js";
import { useNavigate, Outlet } from "react-router-dom";

const PartyPlanDetail = ({ parentPartyPlan }) => {
  const { accountAvatar, accountFullName } = useAccountContext();
  const { selectedPartyPlanId } = useDashboard();
  const navigate = useNavigate();
  const { token } = useAuthContext();
  const [partyPlan, setPartyPlan] = useState(parentPartyPlan || null);
  const [invitations, setInvitations] = useState([]);
  const [isEditing, setIsEditing] = useState(null);
  const [updatedValue, setUpdatedValue] = useState("");
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
          console.log("Fetched specific party plan:", data);
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
            <div className="col start-date">
              {renderEditableField(
                "Start Time",
                partyPlan.start_time.toLowerCase()
              )}
            </div>
          </div>
          <div className="row mb-4">
            <div className="col end-date">
              {renderEditableField(
                "End Time",
                partyPlan.end_time.toLowerCase()
              )}
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
        <div className="col-md-5">
          {/* Description and Keywords */}
          <div className="keywords">{partyPlan.keywords.join(", ")}</div>
          <div className="description mb-3">{partyPlan.description}</div>
        </div>
        <div className="col-md-7">
          {/* Invitations */}
          <div className="invitations-list">
            <div className="invited-subtitle">Your invite list</div>
            <div>
              <ul className="invitations-unstyled-list">
                {invitations.map((invite) => (
                  <li key={invite.id} className="invitation-item">
                    <a href={`mailto:${invite.account.email}`}>
                      {invite.account.fullname}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
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
