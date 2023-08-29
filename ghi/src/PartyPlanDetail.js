import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { baseUrl } from "./common/config.js";

const PartyPlanDetail = ({ parentPartyPlan }) => {
  const { id } = useParams();
  const [partyPlan, setPartyPlan] = useState(parentPartyPlan || null);
  //   const [partyPlan, setPartyPlan] = useState(null);

  useEffect(() => {
    const fetchPartyPlan = async () => {
      try {
        const response = await fetch(`${baseUrl}/party_plans/${id}`);
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

    fetchPartyPlan();
  }, [id]);
  if (!partyPlan) {
    return <div>Loading...</div>;
  }

  return (
    <div className="party-plan-detail">
      <h2>Party Plan Details</h2>

      <div>ID: {partyPlan.id}</div>
      <div>Account ID: {partyPlan.account_id}</div>
      <div>Created: {partyPlan.created}</div>
      <div>Updated: {partyPlan.updated || "N/A"}</div>
      <div>Start Time: {partyPlan.start_time}</div>
      <div>End Time: {partyPlan.end_time}</div>
      <div>Description: {partyPlan.description}</div>
      <div>
        Image: <img src={partyPlan.image} alt="party" />
      </div>
      <div>Party Status: {partyPlan.party_status}</div>
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
            <div>Geo: {location.geo.join(", ")}</div>
            <div>Input: {location.input}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PartyPlanDetail;
