import { Modal, Button } from "react-bootstrap";
import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import React, { useState, useEffect } from "react";
import { baseUrl } from "./utils/config.js";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import { useDateContext } from "./DateContext.js";

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

const InvitationForm = ({ show, onHide }) => {
  const { token } = useAuthContext();
  const [accountId, setAccountId] = useState(account_json._id);
  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = {
      //   account_id: accountId,
      //   api_maps_location: apiMapsLocation,
      //   start_time: new Date(startTime).toISOString(),
      //   end_time: endTime ? new Date(endTime).toISOString() : null,
      //   description,
      //   image,
      //   keywords: keywords.split(",").map((k) => k.trim()),
    };

    const apiUrl = `${baseUrl}/invitations/`;
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
      //   onFormSubmit();
    }
  };

  // check id
  const isValidObjectId = (id) => /^[a-f\d]{24}$/i.test(id);

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Invitation Form</Modal.Title>
      </Modal.Header>
      <Modal.Body>{/* Your form components go here */}</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
        <Button variant="primary">Send Invitation</Button>
      </Modal.Footer>
    </Modal>
  );
};

export default InvitationForm;
