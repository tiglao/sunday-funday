import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

function InviteeDashboard() {
  const { token } = useAuthContext();
  const navigate = useNavigate();
  useEffect(() => {
    if (!token) {
      navigate("/");
    }
  }, [token, navigate]);

  if (!token) {
    return null;
  }

  return (
    <div>
      <h1>Invitee Dashboard</h1>
    </div>
  );
}

export default InviteeDashboard;
