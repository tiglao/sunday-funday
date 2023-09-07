import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { baseUrl } from "./common/config.js";
import SearchComponent from "./Search.jsx";
import GoogleMap from "./GoogleMap";

const PartyPlanDetail = ({ parentPartyPlan }) => {
  const { id } = useParams();
  const [partyPlan, setPartyPlan] = useState(parentPartyPlan || null);

  const keyword = "keyword";
  const location = "location";
  const date = "date";
  const time = "time";

  const handleSearch = () => {
    const fetchDataFromGoogleMapsAPI = async (
      keyword,
      location,
      date,
      time
    ) => {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ keyword, location, date, time }),
      };
      const response = await fetch(
        `${baseUrl}/${id}/search_nearby`,
        requestOptions
      );
      if (response.ok) {
        const data = await response.json();
        const newPartyPlan = {...parentPartyPlan, searched_locations}
      }
    };
  }

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
                    partyPlan.start_time.toLowerCase(),
                  )}
                </div>
              </div>
              <div className="row">
                <div className="col">
                  {renderEditableField(
                    "End Time",
                    partyPlan.end_time.toLowerCase(),
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

            <div>Created: {partyPlan.created}</div>
            <div>Last Updated: {partyPlan.updated || "N/A"}</div>

            <div>{renderEditableField("Start Time", partyPlan.start_time)}</div>
            <div>{renderEditableField("End Time", partyPlan.end_time)}</div>
            <div>
              {renderEditableField("Description", partyPlan.description)}
            </div>
            <div>
              {renderEditableField("Party Status", partyPlan.party_status)}
            </div>
            <div>
              Image: <img src={partyPlan.image} alt="party" />
            </div>
            <div>
              Invitations:{" "}
              {partyPlan.invitations ? partyPlan.invitations.join(", ") : "N/A"}
            </div>

            <div>
              Keywords:{" "}
              {partyPlan.keywords ? partyPlan.keywords.join(", ") : "N/A"}
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
          <GoogleMap />
        </div>
      </div>
    );
  };
};
export default PartyPlanDetail;