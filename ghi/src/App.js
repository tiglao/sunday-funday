import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";
import "./App.css";
import { AuthProvider, useToken } from "@galvanize-inc/jwtdown-for-react";
import UserDashboard from "./UserDashboard";
import Dashboard from "./Dashboard";
import PartyPlanDetail from "./PartyPlanDetail";
import InviteeDashboard from "./InviteeDashboard";
import { DateProvider } from "./DateContext";
import Main from "./Main";
import TestSpa from "./TestSpa";

function App() {
  // const { token } = useToken(); // Assuming useToken is a custom hook you've defined elsewhere

  const domain = /https:\/\/[^/]+/;
  const basename = process.env.PUBLIC_URL.replace(domain, "");
  const baseUrl = process.env.REACT_APP_API_HOST;
  return (
    <BrowserRouter basename={basename}>
      <AuthProvider baseUrl={baseUrl}>
        <DateProvider>
          <Routes>
            <Route path="/" element={<Main />}></Route>
            <Route path="/dashboard" element={<Dashboard />}></Route>
            <Route path="/user_dashboard" element={<UserDashboard />}></Route>
            <Route path="/invitee" element={<InviteeDashboard />}></Route>
            <Route path="/test" element={<TestSpa />}></Route>
          </Routes>
        </DateProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
export default App;
