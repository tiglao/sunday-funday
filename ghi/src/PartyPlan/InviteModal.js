import { Modal, Button } from "react-bootstrap";
import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { useDashboard } from "../utils/DashboardContext.js";
import { useParams } from "react-router-dom";

const InvitationForm = ({ show, onHide, partyPlanId }) => {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const { selectedPartyPlanId } = useParams();

  const handleSubmit = async (event) => {
    event.preventDefault();

    const payload = {
      fullName,
      email,
    };

    const apiUrl = `http://127.0.0.1:8000/invitations/?party_plan_id=${selectedPartyPlanId}`;
    const fetchConfig = {
      method: "POST",
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
    };

    const response = await fetch(apiUrl, fetchConfig);

    if (response.ok) {
      const newInvitation = await response.json();
    } else {
      console.log("Failed to create invitation");
    }
  };

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Invitation Form</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group as={Row}>
            <Form.Label column sm="2">
              Full Name
            </Form.Label>
            <Col sm="10">
              <Form.Control
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </Col>
          </Form.Group>
          <Form.Group as={Row}>
            <Form.Label column sm="2">
              Email
            </Form.Label>
            <Col sm="10">
              <Form.Control
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
          Send Invitation
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default InvitationForm;
