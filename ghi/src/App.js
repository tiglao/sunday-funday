import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import { AuthProvider } from "@galvanize-inc/jwtdown-for-react";
import LoginForm from "./LoginForm";
import UserDashboard from "./UserDashboard";
import Nav from "./Nav";

function App() {
  const domain = /https:\/\/[^/]+/;
  const basename = process.env.PUBLIC_URL.replace(domain, "");
  const baseUrl = process.env.REACT_APP_API_HOST;

  return (
    <BrowserRouter basename={basename}>
      <AuthProvider baseUrl={baseUrl}>
        <Nav />
        <Routes>
          <Route path="/login" element={<LoginForm />}></Route>
          <Route path="/dashboard" element={<UserDashboard />}></Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
export default App;
