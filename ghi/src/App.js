import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import { AuthProvider } from "@galvanize-inc/jwtdown-for-react";
import { DateProvider } from "./DateContext";
import Main from "./Main";
import Dashboard from "./Dashboard";
import UserDashboard from "./UserDashboard";
import PartyPlanForm from "./PartyPlanForm";
import PartyPlanDetail from "./PartyPlanDetail";
import InviteeDashboard from "./InviteeDashboard";
import TestSpa from "./TestSpa";
import UpdateProfile from "./UpdateProfile";
import { DashboardProvider } from "./utils/DashboardContext";
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
            {/* Public route accessible to all */}
            <Route path="/" element={<Main />} />

            {/* Protected routes */}
            <Route
              path="/dashboard/*"
              element={
                <ProtectedRoute
                  element={
                    <DashboardProvider>
                      <Dashboard />
                    </DashboardProvider>
                  }
                />
              }
            >
              {/* Dashboard */}
              <Route index element={<UserDashboard />} />

              {/* Party Plans */}
              <Route
                path="party_plans/new"
                element={<ProtectedRoute element={<PartyPlanForm />} />}
              />
              <Route
                path="party_plans/:id"
                element={<ProtectedRoute element={<PartyPlanDetail />} />}
              />

              {/* Invitee */}
              <Route
                path="invitee"
                element={<ProtectedRoute element={<InviteeDashboard />} />}
              />

              {/* Test and UpdateProfile */}
              <Route
                path="test"
                element={<ProtectedRoute element={<TestSpa />} />}
              />
            </Route>
          </Routes>
        </DateProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
