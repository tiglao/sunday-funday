import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import React, { useEffect, useState } from "react";
import { baseUrl } from "../utils/config.js";
import { FaEdit, FaCheck } from "react-icons/fa";
import { useDashboard } from "../utils/DashboardContext";
import Button from "react-bootstrap/Button";
import InvitationForm from "./InviteModal.js";

const account_json = {
  _id: "64ef6496ef30ab1c58616d1a",
  email: "example@example.com",
  full_name: "Jack Frost",
  date_of_birth: "06/19/1976",
  avatar:
    "https://render.fineartamerica.com/images/images-profile-flow/400/images/artworkimages/mediumlarge/3/open-third-eye-nobodys-hero.jpg",
  username: "example@example.com",
  hashed_password:
    "$2b$12$vsDdjNYiHI9cxvfeO4gzue/NBNbfoE.G32lF68saKOdpJQd/oKQm.",
};

const PartyPlanDetail = ({ parentPartyPlan }) => {
  const { token } = useAuthContext();
  const [accountId, setAccountId] = useState(account_json._id);
  const [accountData, setAccountData] = useState(account_json);
  const { selectedPartyPlanId } = useDashboard();
  const [partyPlan, setPartyPlan] = useState(parentPartyPlan || null);
  const [invitations, setInvitations] = useState([]);
  const [isEditing, setIsEditing] = useState(null);
  const [updatedValue, setUpdatedValue] = useState("");
  const [showInviteModal, setShowInviteModal] = useState(false);
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
    <div className="container">
      <div className="row">
        <div className="col-12">
          <div className="row">
            <div className="col-md-3 text-center">
              <img
                src={partyPlan.image}
                alt={partyPlan.description}
                className="img-fluid rounded"
              />
            </div>
            <div className="col-md-9 align-self-end">
              <div className="row">
                <div className="col">
                  {renderEditableField(
                    "Start Time",
                    partyPlan.start_time.toLowerCase()
                  )}
                </div>
              </div>
              <div className="row">
                <div className="col">
                  {renderEditableField(
                    "End Time",
                    partyPlan.end_time.toLowerCase()
                  )}
                </div>
              </div>
              {/* party planner */}
              <div className="planner-description">
                <div className="planner-image">
                  <img
                    src={accountData.avatar}
                    alt="planner-avatar"
                    className="rounded-square"
                    style={{ width: "70px", height: "70px" }}
                  />
                </div>
                <div className="planner-name">
                  Planned by: {accountData.full_name}
                </div>
              </div>
            </div>
          </div>
          <div className="row mt-4">
            <div className="col-md-3">
              <div>
                <div>{partyPlan.description}</div>
                <div>{partyPlan.keywords}</div>
              </div>
            </div>
            <div className="col-md-9">
              <div>
                <div className="invitations-list">
                  <h5>Invitations</h5>
                  <ul>
                    {invitations.map((invite) => (
                      <li key={invite.id}>
                        <div>
                          Guest: {invite.account.fullname} (
                          {invite.account.email})
                        </div>
                        <div>RSVP Status: {invite.rsvp_status}</div>
                        <div>Sent: {invite.sent_status ? "Yes" : "No"}</div>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <Button variant="primary" onClick={openInviteModal}>
                    Open Invitation Form
                  </Button>
                </div>
              </div>
            </div>
      <div>Created: {partyPlan.created}</div>
      <div>Last Updated: {partyPlan.updated || "N/A"}</div>


      <div>{renderEditableField("Start Time", partyPlan.start_time)}</div>
      <div>{renderEditableField("End Time", partyPlan.end_time)}</div>
      <div>{renderEditableField("Description", partyPlan.description)}</div>
      <div>{renderEditableField("Party Status", partyPlan.party_status)}</div>
      <div>
        Image: <img src={partyPlan.image} alt="party" />
      </div>
      <div>
        Invitations:{" "}
        {partyPlan.invitations ? partyPlan.invitations.join(", ") : "N/A"}
      </div>

      <div>
        Keywords: {partyPlan.keywords ? partyPlan.keywords.join(", ") : "N/A"}
      </div>

      <div>
        Searched Locations:{" "}
        {partyPlan.searched_locations
          ? partyPlan.searched_locations.join(", ")
          : "N/A"}
      </div>
      <div>
        Favorite Locations:{" "}
        {partyPlan.favorite_locations
          ? partyPlan.favorite_locations.join(", ")
          : "N/A"}
      </div>
      <div>
        Chosen Locations:{" "}
        {partyPlan.chosen_locations
          ? partyPlan.chosen_locations.join(", ")
          : "N/A"}
      </div>

      <div>

        <h3>API Maps Location</h3>
        {partyPlan.api_maps_location.map((location, index) => (
          <div key={index}>
            <div>Geo: {location.geo ? location.geo.join(", ") : "N/A"}</div>
            <div>Input: {location.input}</div>
          </div>
        ))}
        </div>
      </div>
      <InvitationForm show={showInviteModal} onHide={toggleInviteModal} />
    </div>
    </div>
    </div>
  );
};

export default PartyPlanDetail;
