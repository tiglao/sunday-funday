import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import React, { useState, useEffect } from "react";
import { baseUrl } from "./utils/config.js";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import { useDateContext } from "./DateContext.js";
import { useNavigate } from 'react-router-dom';
import { useParams } from "react-router-dom";

// import stuff in to use usetoken. for now account data is faked here.
// want to be able to use the token to give the original account model.
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


const PartyPlanForm = ({ onFormSubmit, onCancel }) => {
  const { token } = useAuthContext();
  const [accountId, setAccountId] = useState(account_json._id);
  const [startTime, setStartTime] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState("");
  const [keywords, setKeywords] = useState("");
  const [plans, setPlans] = useState([]);
  const [apiMapsLocation, setApiMapsLocation] = useState([{ input: "" }]);
  const [endTime, setEndTime] = useState("");
  const localDate = useDateContext();
  const {partyplanid} = useParams();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = {
      account_id: accountId,
      api_maps_location: apiMapsLocation,
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

    const navigate = useNavigate();

    const response = await fetch(apiUrl, fetchConfig);
    if (response.ok) {
      const newPartyPlan = await response.json();
      onFormSubmit();

      navigate(`/locations/${partyplanid}/search_nearby`);
    }
  };

  // check id
  const isValidObjectId = (id) => /^[a-f\d]{24}$/i.test(id);


  useEffect(() => {
    if (localDate) {
      const formattedDate = localDate.toISOString().substring(0, 16); // Convert to datetime-local format
      setStartTime(formattedDate);
      setEndTime(formattedDate);
    }
  }, [localDate]);
  useEffect(() => {
    if (isValidObjectId(accountId)) {
      console.log("Valid account ID");
    } else {
      console.log("Invalid account ID");
    }
  }, [accountId]);

  return (
    <Container className="mt-5 text-white" style={{ backgroundColor: "#333" }}>
      <Row>
        <Col className="offset-md-3 col-md-6">
          <div className="shadow p-4" style={{ backgroundColor: "#444" }}>
            <h1>Create a Party Plan</h1>
            <Form onSubmit={handleSubmit} id="create-partyplan-form">
              <Form.Group>
                <Form.Label>Account ID:</Form.Label>
                <Form.Control
                  type="text"
                  value={accountId}
                  onChange={(e) => setAccountId(e.target.value)}
                />
              </Form.Group>

              <Form.Group>
                <Form.Label>API Maps Location (Input):</Form.Label>
                <Form.Control
                  type="text"
                  value={apiMapsLocation[0]?.input}
                  onChange={(e) =>
                    setApiMapsLocation([{ input: e.target.value }])
                  }
                />
              </Form.Group>

              <Form.Group>
                <Form.Label>Start Time:</Form.Label>
                <Form.Control
                  type="datetime-local"
                  value={startTime}
                  onChange={(e) => setStartTime(e.target.value)}
                />
              </Form.Group>

              <Form.Group>
                <Form.Label>End Time:</Form.Label>
                <Form.Control
                  type="datetime-local"
                  value={endTime}
                  onChange={(e) => setEndTime(e.target.value)}
                />
              </Form.Group>

              <Form.Group>
                <Form.Label>Description:</Form.Label>
                <Form.Control
                  as="textarea"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </Form.Group>

              <Form.Group>
                <Form.Label>Image URL:</Form.Label>
                <Form.Control
                  type="url"
                  value={image}
                  onChange={(e) => setImage(e.target.value)}
                />
              </Form.Group>

              <Form.Group>
                <Form.Label>Keywords (comma-separated):</Form.Label>
                <Form.Control
                  type="text"
                  value={keywords}
                  onChange={(e) => setKeywords(e.target.value)}
                />
              </Form.Group>

              <Button onClick={handleTestNavigation} variant="primary" type="submit">
                Create
              </Button>
              <Button onClick={handleTestNavigation}>Test Navigation</Button>
              <Button
                variant="secondary"
                onClick={onCancel}
                style={{
                  marginLeft: "10px",
                  fontSize: "0.8em",
                }}
              >
                Cancel
              </Button>
            </Form>
          </div>
        </Col>
      </Row>
    </Container>
  );
  // <div className="row">
  //   <div className="offset-3 col-6">
  //     <div className="shadow p-4 mt-4">
  //       <h1>Create a Party Plan</h1>
  //       <form onSubmit={handleSubmit} id="create-partyplan-form">
  //         <label>
  //           Account ID:
  //           <input
  //             type="text"
  //             value={accountId}
  //             onChange={(e) => setAccountId(e.target.value)}
  //           />
  //         </label>

  //         <label>
  //           API Maps Location (Input):
  //           <input
  //             type="text"
  //             value={apiMapsLocation[0].input}
  //             onChange={(e) =>
  //               setApiMapsLocation([{ input: e.target.value }])
  //             }
  //           />
  //         </label>

  //         <label>
  //           Start Time:
  //           <input
  //             type="datetime-local"
  //             value={startTime}
  //             onChange={(e) => setStartTime(e.target.value)}
  //           />
  //         </label>

  //         <label>
  //           End Time:
  //           <input
  //             type="datetime-local"
  //             value={endTime}
  //             onChange={(e) => setEndTime(e.target.value)}
  //           />
  //         </label>

  //         <label>
  //           Description:
  //           <textarea
  //             value={description}
  //             onChange={(e) => setDescription(e.target.value)}
  //           />
  //         </label>

  //         <label>
  //           Image URL:
  //           <input
  //             type="url"
  //             value={image}
  //             onChange={(e) => setImage(e.target.value)}
  //           />
  //         </label>

  //         <label>
  //           Keywords (comma-separated):
  //           <input
  //             type="text"
  //             value={keywords}
  //             onChange={(e) => setKeywords(e.target.value)}
  //           />
  //         </label>
  //         <button className="btn btn-primary" type="submit">
  //           Create
  //         </button>
  //         <a
  //           href="#"
  //           onClick={onCancel}
  //           style={{
  //             marginLeft: "10px",
  //             color: "gray",
  //             fontSize: "0.8em",
  //             textDecoration: "none",
  //           }}
  //         >
  //           Cancel
  //         </a>
  //       </form>
  //     </div>
  //   </div>
  // </div>
  //   );
};

export default PartyPlanForm;
