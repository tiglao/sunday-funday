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
import UpdateProfile from "./UpdateProfile";
import PartyPlanForm from "./PartyPlanForm";
import { DashboardProvider } from "./utils/DashboardContext";
import { useNavigate } from "react-router-dom";
import ProtectedRoute from "./ProtectedRoute";

function App() {
  const domain = /https:\/\/[^/]+/;
  const basename = process.env.PUBLIC_URL.replace(domain, "");
  const baseUrl = process.env.REACT_APP_API_HOST;

  return (
    <BrowserRouter basename={basename}>
      <AuthProvider baseUrl={baseUrl}>
        <DateProvider>
          <Routes>
            <Route path="/" element={<Main />} />
            <Route
              path="/dashboard/*"
              element={
                <ProtectedRoute
                  component={() => (
                    <DashboardProvider>
                      <Dashboard />
                    </DashboardProvider>
                  )}
                />
              }
            >
              <Route index element={<UserDashboard />} />
              <Route path="party_plans/new" element={<PartyPlanForm />} />
              <Route path="party_plans/:id" element={<PartyPlanDetail />} />
            </Route>
            <Route
              path="/invitee"
              element={<ProtectedRoute component={InviteeDashboard} />}
            />
            <Route
              path="/test"
              element={<ProtectedRoute component={TestSpa} />}
            />
            <Route
              path="/UpdateProfile"
              element={<ProtectedRoute component={UpdateProfile} />}
            />
          </Routes>
        </DateProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
