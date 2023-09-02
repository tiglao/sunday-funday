import React, { useEffect, useState } from "react";
import { baseUrl } from "./utils/config.js";
import { FaEdit, FaCheck } from "react-icons/fa";
import { useDashboard } from "./utils/DashboardContext";

const PartyPlanDetail = ({ parentPartyPlan }) => {
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
    <div className="party-plan-detail">
      <h2>Party Plan Details</h2>

      <div>Created: {partyPlan.created}</div>
      <div>Last Updated: {partyPlan.updated || "N/A"}</div>

      {/* EDITABLE */}
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
        {/* EDITABLE BUT ONLY INPUT */}
        <h3>API Maps Location</h3>
        {partyPlan.api_maps_location.map((location, index) => (
          <div key={index}>
            <div>Geo: {location.geo ? location.geo.join(", ") : "N/A"}</div>
            <div>Input: {location.input}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PartyPlanDetail;
