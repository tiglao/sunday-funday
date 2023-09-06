import React, { useState, useEffect } from "react";
import { Modal, Button, Form, Row, Col } from "react-bootstrap";
import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useDashboard } from "./utils/DashboardContext.js";
import { baseUrl } from "./utils/config.js";

export const PartyPlanModal = ({ show, onHide }) => {
  const { token } = useAuthContext();
  const [accountId, setAccountId] = useState("");
  const [description, setDescription] = useState("");
  const { selectedPartyPlanId } = useDashboard();
  const [startTime, setStartTime] = useState("");
  const [image, setImage] = useState("");
  const [keywords, setKeywords] = useState("");
  const [plans, setPlans] = useState([]);
  const [location, setLocation] = useState("");
  const [endTime, setEndTime] = useState("");
  const [showModal, setShowModal] = useState(false);

  const handleSubmit = async (event) => {
    console.log("handleSubmit called");
    event.preventDefault();
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
    const apiUrl = `${baseUrl}/party_plans/`;
    const fetchConfig = {
      method: "post",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    };

    const response = await fetch(apiUrl, fetchConfig);

    if (response.ok) {
      const newPartyPlan = await response.json();
      console.log("Party Plan created:", newPartyPlan);
    } else {
      console.log("Failed to create party plan");
    }
  };

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Create New Party Plan</Modal.Title>
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

          {/* Additional Form Groups for other fields */}
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
          Create
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
