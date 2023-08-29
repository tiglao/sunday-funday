import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";
import "./App.css";
import { AuthProvider, useToken } from "@galvanize-inc/jwtdown-for-react";
import UserDashboard from "./UserDashboard";
import InviteeDashboard from "./InviteeDashboard";
import { DateProvider } from "./DateContext";
import Nav from "./Nav";
import Main from "./Main";
import Account from "./Account";

function App() {
  const [userData, setUserData] = useState({});
  // const { token } = useToken(); // Assuming useToken is a custom hook you've defined elsewhere

  const domain = /https:\/\/[^/]+/;
  const basename = process.env.PUBLIC_URL.replace(domain, "");
  const baseUrl = process.env.REACT_APP_API_HOST;

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
  }, []);
  console.log(userData);
  return (
    <BrowserRouter basename={basename}>
      <AuthProvider baseUrl={baseUrl}>
        <Nav />
        <DateProvider>
          <Routes>
            <Route path="/" element={<Main />}></Route>
            <Route path="/dashboard" element={<UserDashboard />}></Route>
            <Route
              path="/account"
              element={
                <Account userData={userData} setUserData={setUserData} />
              }
            ></Route>
            <Route path="/invitee" element={<InviteeDashboard />}></Route>
          </Routes>
        </DateProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
export default App;
