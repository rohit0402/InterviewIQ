import { Navigate, Outlet } from "react-router-dom";
import { useSelector } from "react-redux";

function ProtectedRoute() {
    const { accessToken, user } = useSelector((state) => state.auth);

    console.log("ProtectedRoute");
    console.log("accessToken:", accessToken);
    console.log("user:", user);

    if (!accessToken) {
        console.log("➡️ Redirecting: no access token");
        return <Navigate to="/" replace />;
    }

    if (!user?.is_verified) {
        console.log("➡️ Redirecting: user not verified");
        return <Navigate to="/verify-email" replace />;
    }

    return <Outlet />;
}

export default ProtectedRoute;