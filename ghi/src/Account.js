import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const UpdateProfile = () => {
  const [userData, setUserData] = useState({});
  const [profileData, setProfileData] = useState({
    full_name: "",
    date_of_birth: "",
    avatar: "",
    email: "", // Not editable but displayed
  });

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
      email: profileData.email, // Add this line
    };

    const profileUrl = `http://localhost:8000/updateByEmail?email=${profileData.username}`;
    // const url = `${process.env.REACT_APP_API_HOST}/token`;
    const fetchConfig = {
      method: "PUT",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    };

    const response = await fetch(profileUrl, fetchConfig);
    const responseData = await response.json();
    console.log("Response data:", responseData);
    // if (response.ok) {
    //   navigate(`/profile/${profileData.username}`);
    // }
  };

  useEffect(() => {
    const handleGetLoggedInUser = async () => {
      try {
        const url = `${process.env.REACT_APP_API_HOST}/token`;
        const response = await fetch(url, {
          credentials: "include",
        });
        const data = await response.json();
        if (data && data.account) {
          setUserData(data.account);
        }
      } catch (error) {
        console.error(error);
      }
    };

    handleGetLoggedInUser();
    setProfileData((prevState) => ({
      ...prevState,
      ...userData,
    }));
  }, [userData]);

  return (
    <div className="flex flex-col justify-center items-center">
      <h1 className="mt-3">Update Your Profile</h1>
      <div className="w-60 rounded-lg bg-slate-700 flex flex-col justify-center items-center p-4 mt-4 drop-shadow-lg">
        <div className="email-display">
          <strong>Email: </strong>
          {profileData.username}
        </div>
        <form onSubmit={handleSubmit}>
          <div className="">
            <input
              onChange={handleProfileChange}
              placeholder="Email"
              type="email"
              name="email"
              value={profileData.email}
            />
          </div>
          <div className="">
            <input
              onChange={handleProfileChange}
              placeholder="Full Name"
              type="text"
              name="full_name"
              value={profileData.full_name}
            />
          </div>
          <div className="">
            <input
              onChange={handleProfileChange}
              placeholder="Date of Birth"
              type="date"
              name="date_of_birth"
              value={profileData.date_of_birth}
            />
          </div>
          <div className="">
            <input
              onChange={handleProfileChange}
              placeholder="Avatar URL"
              type="url"
              name="avatar"
              value={profileData.avatar}
            />
          </div>
          <button type="submit">Update</button>
        </form>
      </div>
    </div>
  );
};

export default UpdateProfile;
