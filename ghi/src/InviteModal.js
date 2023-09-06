import { Modal, Button } from "react-bootstrap";
import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import React, { useState, useEffect } from "react";
import { baseUrl } from "./utils/config.js";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import { useDateContext } from "./DateContext.js";
import { useDashboard } from "./utils/DashboardContext.js";

const account_json = {
  _id: "64ef6532ef30ab1c58616d1b",
  email: "test@test.com",
  full_name: "Test Testerson",
  date_of_birth: null,
  avatar: null,
  username: "test@test.com",
  hashed_password:
    "$2b$12$K5mQBUZCaWXIz3FTAR8cROll5WcAWXtmeYvnYIRmFNXXMA8PfW.1S",
};

const InvitationForm = ({ show, onHide, partyPlanId }) => {
  const { token } = useAuthContext();
  const [accountId, setAccountId] = useState(account_json._id);
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const { selectedPartyPlanId } = useDashboard();
  console.log(
    `This modal has successfully received the selectedPartyPlanId: ${selectedPartyPlanId}`
  );

  const dummyAccountId = "123e4567-e89b-12d3-a456-426614174001";
  const handleSubmit = async (event) => {
    event.preventDefault();

    const payload = {
      fullName,
      email,
    };

    console.log("JSON payload:", JSON.stringify(payload));
    const apiUrl = `http://127.0.0.1:8000/invitations/?party_plan_id=${selectedPartyPlanId}`;
    console.log("check URL:", apiUrl);
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
      console.log("Invitation created:", newInvitation);
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
