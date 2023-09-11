import React, { useState } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const FeedbackModal = ({ show, handleClose }) => {
  const [feedback, setFeedback] = useState("");
  const [name, setName] = useState("");
  const handleSubmit = () => {
    handleClose();
    const emailBody = `
      Hey Team,


      Here's what I think would make Sunday Funday a better product:

      ${feedback}


      What do y'all think?


      Best,

      [Your Name]
    `;
    const encodedBody = encodeURIComponent(emailBody);

    window.location.href = `mailto:support@example.com?subject=Feedback&body=${encodedBody}`;
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>What's on your mind?</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group
            className="mb-3"
            controlId="feedbackForm.ControlInputName"
          >
            <Form.Label>Your Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId="feedbackForm.ControlTextarea">
            <Form.Label>Please enter your feedback</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
            />
          </Form.Group>
        </Form>
        <>
          <small>
            Submitting this form will send an email to us from your preferred
            email client.
          </small>
        </>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={handleSubmit}>
          Submit
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default FeedbackModal;
