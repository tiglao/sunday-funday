import React, { createContext, useContext, useState, useEffect } from "react";
import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";

const AccountContext = createContext();

export const useAccountContext = () => {
  const context = useContext(AccountContext);
  if (!context) {
    throw new Error(
      "useAccountContext must be used within an AccountContextProvider"
    );
  }
  return context;
};

export const AccountContextProvider = ({ children }) => {
  const { token } = useAuthContext();
  const [accountId, setAccountId] = useState(null);
  const [accountEmail, setAccountEmail] = useState(null);
  const [accountFullName, setAccountFullName] = useState(null);
  const [accountAvatar, setAccountAvatar] = useState(null);
  const [accountDateOfBirth, setAccountDateOfBirth] = useState(null);

  useEffect(() => {
    if (token) {
      const decodedToken = JSON.parse(atob(token.split(".")[1]));

      if (decodedToken && decodedToken.account) {
        setAccountId(decodedToken.account.id);
        setAccountEmail(decodedToken.account.username);
        setAccountFullName(decodedToken.account.full_name);

        const fetchAccountDetails = async () => {
          const apiUrl = `http://127.0.0.1:8000/accountByEmail?email=${decodedToken.account.username}`;
          const response = await fetch(apiUrl);
          if (response.ok) {
            const accountData = await response.json();
            setAccountAvatar(accountData.avatar);
            setAccountDateOfBirth(accountData.date_of_birth);
          }
        };

        fetchAccountDetails();
      }
    }
  }, [token]);

  return (
    <AccountContext.Provider
      value={{
        accountId,
        accountEmail,
        accountFullName,
        accountAvatar,
        accountDateOfBirth,
      }}
    >
      {children}
    </AccountContext.Provider>
  );
};
