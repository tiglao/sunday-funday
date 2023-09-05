import useToken from "@galvanize-inc/jwtdown-for-react";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ component: Component }) {
  const { token } = useToken();

  return token ? <Component /> : <Navigate to="/" replace />;
}

export default ProtectedRoute;
