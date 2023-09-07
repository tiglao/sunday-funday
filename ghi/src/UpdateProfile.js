import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const UpdateProfile = ({ handleUpdateProfileClose }) => {
  const [userData, setUserData] = useState({});
  const [profileData, setProfileData] = useState({
    full_name: "",
    date_of_birth: "",
    avatar: "",
    email: "",
    username: "",
  });

  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const navigate = useNavigate();

  const handleProfileChange = (event) => {
    setProfileData({
      ...profileData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = {
      full_name: profileData.full_name,
      date_of_birth: profileData.date_of_birth,
      avatar: profileData.avatar,
      email: profileData.email,
      username: profileData.email,
    };

    const profileUrl = `http://localhost:8000/updateByEmail?email=${profileData.username}`;
    const fetchConfig = {
      method: "PUT",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    };

    try {
      const response = await fetch(profileUrl, fetchConfig);
      const responseData = await response.json();
      console.log("Response data:", responseData);
      if (response.ok) {
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const handleGetLoggedInUser = async () => {
      try {
        const url = `${process.env.REACT_APP_API_HOST}/token`;
        const response = await fetch(url, {
          credentials: "include",
        });
        const data = await response.json();
        console.log("Fetched data:", data);
        if (data && data.account) {
          setUserData(data.account);
          setProfileData((prevState) => ({
            ...prevState,
            ...Object.fromEntries(
              Object.entries(data.account).map(([key, value]) => [
                key,
                value ?? "",
              ])
            ),
            username: data.account.email,
          }));

          const additionalDataUrl = `http://localhost:8000/accountByEmail?email=${data.account.username}`;
          const additionalDataResponse = await fetch(additionalDataUrl);
          const additionalData = await additionalDataResponse.json();
          console.log("Additional data fetched:", additionalData);

          if (additionalData) {
            setProfileData((prevState) => ({
              ...prevState,
              ...Object.fromEntries(
                Object.entries(additionalData).map(([key, value]) => [
                  key,
                  value ?? "",
                ])
              ),
            }));
          }
        }
      } catch (error) {
        console.error(error);
      }
    };

    handleGetLoggedInUser();
  }, []);

  return (
    <div className="flex flex-col justify-center items-center">
      <div className="w-60 rounded-lg bg-slate-700 flex flex-col justify-center items-center p-4 mt-4 drop-shadow-lg">
        <Modal.Header closeButton>
          <Modal.Title className="text-center">Update profile</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group
              className="mb-3"
              controlId="updateProfileForm.ControlInput1"
            >
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                name="email"
                value={profileData.email}
                onChange={handleProfileChange}
                disabled
              />
            </Form.Group>
            <Form.Group
              className="mb-3"
              controlId="updateProfileForm.ControlInput2"
            >
              <Form.Label>Full Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter your full name"
                name="full_name"
                value={profileData.full_name}
                onChange={handleProfileChange}
                disabled
              />
            </Form.Group>
            <Form.Group
              className="mb-3"
              controlId="updateProfileForm.ControlInput3"
            >
              <Form.Label>Date of Birth</Form.Label>
              <Form.Control
                type="date"
                name="date_of_birth"
                value={profileData.date_of_birth}
                onChange={handleProfileChange}
              />
            </Form.Group>
            <Form.Group
              className="mb-3"
              controlId="updateProfileForm.ControlInput4"
            >
              <Form.Label>Avatar URL</Form.Label>
              <Form.Control
                type="url"
                placeholder="Enter Avatar URL"
                name="avatar"
                value={profileData.avatar}
                onChange={handleProfileChange}
              />
            </Form.Group>
            <Modal.Footer>
              <Button variant="secondary" onClick={handleUpdateProfileClose}>
                Close
              </Button>
              <Button
                variant="primary"
                type="submit"
                onClick={handleUpdateProfileClose}
              >
                Update
              </Button>
            </Modal.Footer>
          </Form>
        </Modal.Body>
      </div>
    </div>
  );
};

export default UpdateProfile;
