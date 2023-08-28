import React, { createContext, useContext, useState, useEffect } from "react";

const DateContext = createContext();

export function useDateContext() {
  return useContext(DateContext);
}

export function DateProvider({ children }) {
  const [localDate, setLocalDate] = useState(null);

  useEffect(() => {
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const utcDate = new Date("2023-08-25T02:56:43.950Z");
    const localDate = new Date(
      utcDate.toLocaleString("en-US", { timeZone: timeZone })
    );
    setLocalDate(localDate);
  }, []);

  return (
    <DateContext.Provider value={localDate}>{children}</DateContext.Provider>
  );
}

export default useDateContext;
