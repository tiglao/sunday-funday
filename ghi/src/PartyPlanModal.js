import React, { useState, useEffect } from "react";
import { Modal, Button, Form, Row, Col } from "react-bootstrap";
import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useDashboard } from "./utils/DashboardContext.js";

export const PartyPlanModal = ({ show, handleClose, partyPlanId }) => {
  const { token } = useAuthContext();
  const [accountId, setAccountId] = useState("");
  const [description, setDescription] = useState("");
  const { selectedPartyPlanId } = useDashboard();

  const handleSubmit = async (event) => {
    event.preventDefault();

    const payload = {
      accountId,
      description,
    };

    const apiUrl = `http://127.0.0.1:8000/party_plans/?party_plan_id=${selectedPartyPlanId}`;
    const fetchConfig = {
      method: "POST",
      body: JSON.stringify(payload),
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
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Create New Party Plan</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group as={Row}>
            <Form.Label column sm="2">
              Account ID
            </Form.Label>
            <Col sm="10">
              <Form.Control
                type="text"
                value={accountId}
                onChange={(e) => setAccountId(e.target.value)}
              />
            </Col>
          </Form.Group>
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
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={handleSubmit}>
          Create
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
