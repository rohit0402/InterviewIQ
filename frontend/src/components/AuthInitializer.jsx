import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { refresh, getCurrentUser } from "../api/authApi";
import { setCredentials,setInitialized } from "../features/auth/authSlice";

export default function AuthInitializer({ children }) {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function restoreSession() {
      try {
        const tokenResponse = await refresh();
        const user = await getCurrentUser();

        dispatch(
          setCredentials({
            accessToken: tokenResponse.access_token,
            user,
          })
        );
      } catch {
        dispatch(setInitialized());
      } finally {
        setLoading(false);
      }
    }

    restoreSession();
  }, [dispatch]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return children;
}