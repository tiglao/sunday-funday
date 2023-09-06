import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import React, { useEffect, useState } from "react";
import { baseUrl } from "./utils/config.js";
import { FaEdit, FaCheck } from "react-icons/fa";
import { useDashboard } from "./utils/DashboardContext";

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
  const [isEditing, setIsEditing] = useState(null);
  const [updatedValue, setUpdatedValue] = useState("");

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
    <div className="container">
      <div className="row">
        <div className="col-12">
          {/* image/info row */}
          <div className="row">
            {/* party image*/}
            <div className="col-md-3 text-center">
              <img
                src={partyPlan.image}
                alt={partyPlan.description}
                className="img-fluid rounded"
              />
            </div>
            {/* basic info*/}
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
          {/* more info/invitations row */}
          <div className="row mt-4">
            {/* description */}

            <div className="col-md-3">
              <div>
                <div>{partyPlan.description}</div>
                <div>{partyPlan.keywords}</div>
              </div>
            </div>
            {/* invitations */}
            <div className="col-md-9">
              <div>
                <div>invitations</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PartyPlanDetail;
