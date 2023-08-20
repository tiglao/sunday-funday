import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import { AuthProvider } from "@galvanize-inc/jwtdown-for-react";
import UserDashboard from "./UserDashboard";
import InviteeDashboard from "./InviteeDashboard";
import Nav from "./Nav";
import Main from "./Main";

function App() {
  const domain = /https:\/\/[^/]+/;
  const basename = process.env.PUBLIC_URL.replace(domain, "");
  const baseUrl = process.env.REACT_APP_API_HOST;

  return (
    <BrowserRouter basename={basename}>
      <AuthProvider baseUrl={baseUrl}>
        <Nav />
        <Routes>
          <Route path="/" element={<Main />}></Route>
          <Route path="/dashboard" element={<UserDashboard />}></Route>
          <Route path="/invitee" element={<InviteeDashboard />}></Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
export default App;
