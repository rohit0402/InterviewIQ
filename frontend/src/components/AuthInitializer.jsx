import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { refresh, getCurrentUser } from "../api/authApi";
import { setCredentials, setInitialized } from "../features/auth/authSlice";

export default function AuthInitializer({ children }) {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function restoreSession() {
      console.log("1. restoreSession started");

      try {
        const tokenResponse = await refresh();
        console.log("2. refresh success", tokenResponse);

        const user = await getCurrentUser();
        console.log("3. user success", user);

        dispatch(
          setCredentials({
            accessToken: tokenResponse.access_token,
            user,
          }),
        );

        console.log("4. dispatched");
      } catch (e) {
        console.error("restoreSession error", e);
      } finally {
        console.log("5. loading false");
        setLoading(false);
      }
    }

    restoreSession();
  }, [dispatch]);
  useEffect(() => {
    async function restoreSession() {
      try {
        const tokenResponse = await refresh();
        const user = await getCurrentUser();

        dispatch(
          setCredentials({
            accessToken: tokenResponse.access_token,
            user,
          }),
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
