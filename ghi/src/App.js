import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import { AuthProvider } from "@galvanize-inc/jwtdown-for-react";
import LoginForm from "./utils/LoginForm";
import Nav from "./Nav";

function App() {
  // other stuff, here

  return (
    <BrowserRouter>
      <AuthProvider>
        <Nav />
        <Routes>
          <Route path="/login" element={<LoginForm />}></Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
export default App;
