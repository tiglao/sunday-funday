import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useDateContext } from "../utils/DateContext";

function InviteeDashboard() {
  const { token } = useAuthContext();
  const navigate = useNavigate();
  const localDate = useDateContext();

  useEffect(() => {
    if (!token) {
      navigate("/");
    }
  }, [token, navigate]);

  if (!token) {
    return null;
  }

  return (
    <div className="text-center">
      <h1>Example</h1>
      <div>{localDate ? localDate.toString() : "Loading date..."}</div>
    </div>
  );
}

export default InviteeDashboard;
