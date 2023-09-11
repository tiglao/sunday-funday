import React, { useState, useEffect } from "react";
import { Modal, Button, Form, Row, Col } from "react-bootstrap";
import { baseUrl } from "../utils/config.js";
import { useNavigate } from 'react-router-dom';
import { useParams } from "react-router-dom";
import { useAccountContext } from "../utils/AccountContext.js";

export const PartyPlanForm = ({
  show,
  onHide,
  partyPlanData,
  refreshDashboard,
}) => {
  const navigate = useNavigate();
  // const { token } = useAuthContext();
  const { accountId } = useAccountContext();

  const [description, setDescription] = useState("");
  const [startTime, setStartTime] = useState("");
  const [image, setImage] = useState("");
  const [keywords, setKeywords] = useState("");
  const [location, setLocation] = useState("");
  const [endTime, setEndTime] = useState("");
  const [jsonResponse, setJsonResponse] = useState(null);
  const {partyplanid} = useParams();

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("Submit button clicked!");
    const data = {
      account_id: accountId,
      api_maps_location: [
        {
          input: location,
        },
      ],
      start_time: new Date(startTime).toISOString(),
      end_time: endTime ? new Date(endTime).toISOString() : null,
      description,
      image,
      keywords: keywords.split(",").map((k) => k.trim()),
    };
    console.log("Submitting data:", data);

    let apiUrl = `${baseUrl}/party_plans/`;
    let formMethod = "post";

    if (partyPlanData) {
      apiUrl = `${baseUrl}/party_plans/${partyPlanData.id}/`;
      formMethod = "put";
    }

    const fetchConfig = {
      method: formMethod,
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    };

    // const response = await fetch(apiUrl, fetchConfig);

    // if (response.ok) {
    //   const jsonResponse = await response.json();
    //   console.log("API Response:", jsonResponse);
    //   refreshDashboard();
    // } else {
    //   console.log("Failed to create party plan");
    // }

    console.log("Fetching API with config:", fetchConfig); // Debugging

    fetch(apiUrl, fetchConfig)
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          console.log(
            "Failed to create party plan. HTTP Status:",
            response.status
          ); // Debugging
          return null;
        }
      })
      .then((jsonResponse) => {
        if (jsonResponse) {
          const createdParty = jsonResponse;
          const createdPartyId = createdParty.id
          console.log("API Response:", jsonResponse); // Debugging
          refreshDashboard();
          navigate(`/locations/${jsonResponse.id}/search_nearby`);

        }
      })
      .catch((error) => {
        console.log("Fetch error:", error); // Debugging
      });
  };


  useEffect(() => {
    if (partyPlanData) {
      setDescription(partyPlanData.description || "");
      setStartTime(partyPlanData.start_time || "");
      setEndTime(partyPlanData.end_time || "");
      setLocation(partyPlanData.api_maps_location[0].input || "");
      setImage(partyPlanData.image || "");
      setKeywords(
        partyPlanData.keywords ? partyPlanData.keywords.join(", ") : ""
      );
    }
  }, [partyPlanData]);

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Plan Your Party</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group as={Row}>
            <Form.Label column sm="2">
              Description
            </Form.Label>
            <Col sm="10">
              <Form.Control
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </Col>
          </Form.Group>

          <Form.Group as={Row}>
            <Form.Label column sm="2">
              Location
            </Form.Label>
            <Col sm="10">
              <Form.Control
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              />
            </Col>
          </Form.Group>

          <Form.Group as={Row}>
            <Form.Label column sm="2">
              Start Time
            </Form.Label>
            <Col sm="10">
              <Form.Control
                type="datetime-local"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
              />
            </Col>
          </Form.Group>

          <Form.Group as={Row}>
            <Form.Label column sm="2">
              End Time
            </Form.Label>
            <Col sm="10">
              <Form.Control
                type="datetime-local"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
              />
            </Col>
          </Form.Group>

          <Form.Group as={Row}>
            <Form.Label column sm="2">
              Image URL
            </Form.Label>
            <Col sm="10">
              <Form.Control
                type="text"
                value={image}
                onChange={(e) => setImage(e.target.value)}
              />
            </Col>
          </Form.Group>

          <Form.Group as={Row}>
            <Form.Label column sm="2">
              Keywords
            </Form.Label>
            <Col sm="10">
              <Form.Control
                type="text"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
              />
            </Col>
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
        <Button variant="primary" onClick={handleSubmit}>
          Submit
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
