import useToken from "@galvanize-inc/jwtdown-for-react";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ element, ...rest }) {
  const { token } = useToken();

  return token ? element : <Navigate to="/" replace />;
}

export default ProtectedRoute;
