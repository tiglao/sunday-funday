import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import { AuthProvider } from "@galvanize-inc/jwtdown-for-react";
import { DateProvider } from "./utils/DateContext";
import UserDashboard from "./Dashboard/UserDashboard";
import Dashboard from "./Dashboard/Dashboard";
import PartyPlanDetail from "./PartyPlan/PartyPlanDetail";
import Main from "./Main";
import SearchResult from "./SearchResults";
import ProtectedRoute from "./ProtectedRoute";
import { AccountContextProvider } from "./utils/AccountContext";

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
                    <AccountContextProvider>
                      <Dashboard />
                    </AccountContextProvider>
                  }
                />
              }
            >
              <Route index element={<UserDashboard />} />
              <Route
                path="party_plans/:id"
                element={<ProtectedRoute element={<PartyPlanDetail />} />}
              />
            </Route>

            <Route path="/locations/:partyplanid/search_nearby" element={<SearchResult />} />
              {/* <Route
                path="party_plans/:partyplanid"
                element={<PartyPlanDetail />} /> */}

          </Routes>
        </DateProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
