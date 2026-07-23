import { useEffect, useState } from "react";
import { refreshToken } from "../utils/auth";

function AuthInitializer({ children }) {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const initialize = async () => {
            try {
                await refreshToken();
            }
            catch {

            } finally {
                setLoading(false);
            }
        };
        initialize();
    }
        , []);

    if (loading) {
        return (
            <div className="flex h-screen items-center justify-center">
                Loading...
            </div>
        );
    }
    return children;
}

export default AuthInitializer;