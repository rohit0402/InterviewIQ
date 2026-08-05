import { Navigate, Outlet } from "react-router-dom";
import { useSelector } from "react-redux";

function ProtectedRoute() {
    const { accessToken, user,intialized } = useSelector((state) => state.auth);

    if (!intialized) {
        return <div>Loading...</div>;
    }

    if (!accessToken) {
        return <Navigate to="/" replace />;
    }

    if (!user?.is_verified) {
        return <Navigate to="/verify-email" replace />;
    }

    return <Outlet />;
}

export default ProtectedRoute;