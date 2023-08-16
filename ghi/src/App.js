import { useEffect, useState } from "react";
import Construct from "./Construct.js";
import ErrorNotification from "./ErrorNotification";
import "./App.css";
import { AuthProvider } from "@galvanize-inc/jwtdown-for-react";

function App() {
  // other stuff, here

  return (
    <AuthProvider>{/* All of your other components, here */}</AuthProvider>
  );
}
export default App;
