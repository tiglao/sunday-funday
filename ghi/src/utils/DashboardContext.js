import React, { createContext, useContext, useEffect, useState } from "react";

const DashboardContext = createContext();

export const useDashboard = () => {
  return useContext(DashboardContext);
};

export function DashboardProvider({ children }) {
  const [currentView, setCurrentView] = useState("userDashboard");
  const [selectedPartyPlanId, setSelectedPartyPlanId] = useState(null);

  const showPartyPlanDetail = (partyPlanId) => {
    console.log("showPartyPlanDetail called with ID:", partyPlanId);
    setSelectedPartyPlanId(partyPlanId);
    setCurrentView("partyPlanDetail");
  };

  useEffect(() => {
    console.log("After setting, selectedPartyPlanId:", selectedPartyPlanId);
  }, [selectedPartyPlanId]);

  useEffect(() => {
    console.log("After setting, currentView:", currentView);
  }, [currentView]);

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
