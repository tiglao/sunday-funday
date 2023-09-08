import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import { AuthProvider } from "@galvanize-inc/jwtdown-for-react";
import { DateProvider } from "./utils/DateContext";
import UserDashboard from "./Dashboard/UserDashboard";
import Dashboard from "./Dashboard/Dashboard";
import PartyPlanForm from "./PartyPlan/PartyPlanForm";
import PartyPlanDetail from "./PartyPlan/PartyPlanDetail";
import InviteeDashboard from "./Dashboard/InviteeDashboard";
import Main from "./Main";
import TestSpa from "./Tests/TestSpa";
import { DashboardProvider } from "./utils/DashboardContext";
import SearchResult from "./SearchResults";
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
              <Route index element={<UserDashboard />} />
              <Route
                path="party_plans/new"
                element={<ProtectedRoute element={<PartyPlanForm />} />}
              />
              <Route
                path="party_plans/:id"
                element={<ProtectedRoute element={<PartyPlanDetail />} />}
              />
              <Route
                path="invitee"
                element={<ProtectedRoute element={<InviteeDashboard />} />}
              />
              <Route
                path="test"
                element={<ProtectedRoute element={<TestSpa />} />}
              />
            </Route>
            <Route path="/locations/:partyplanid/search_nearby" element={<SearchResult />} />
          </Routes>
        </DateProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
