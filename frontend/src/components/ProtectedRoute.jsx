import { Navigate, Outlet } from "react-router-dom";
import { useSelector } from "react-redux";


// suppose children in dashboard then if you call dashboard it goes to this protected route first and check if user is authenticated
// if not then it redirects to login page else it renders to children
function ProtectedRoute() {
  const { accessToken } = useSelector((state) => state.auth);

  return accessToken ? <Outlet /> : <Navigate to="/" replace />;
}

export default ProtectedRoute;