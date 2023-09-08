import React, { createContext, useContext, useEffect, useState } from "react";

const DashboardContext = createContext();

export const useDashboard = () => {
  return useContext(DashboardContext);
};

export function DashboardProvider({ children }) {
  const [currentView, setCurrentView] = useState("userDashboard");
  const [selectedPartyPlanId, setSelectedPartyPlanId] = useState(null);

  const showPartyPlanDetail = (partyPlanId) => {
    setSelectedPartyPlanId(partyPlanId);
    setCurrentView("partyPlanDetail");
  };

  useEffect(() => {}, [selectedPartyPlanId]);

  useEffect(() => {}, [currentView]);

  const value = {
    currentView,
    setCurrentView,
    selectedPartyPlanId,
    setSelectedPartyPlanId,
    showPartyPlanDetail,
  };

  return (
    <DashboardContext.Provider value={value}>
      {children}
    </DashboardContext.Provider>
  );
}
