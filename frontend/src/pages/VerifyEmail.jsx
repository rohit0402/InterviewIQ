import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { verifyEmail } from "../api/authApi";
import ResendVerification from "../components/auth/ResendVerification";

export default function VerifyEmail() {

    const [params] = useSearchParams();

    const token = params.get("token");

    const [loading, setLoading] = useState(true);

    const [success, setSuccess] = useState(false);

    const [error, setError] = useState("");

    useEffect(() => {

        if (!token) {

            setLoading(false);

            setError("Verification token missing.");

            return;
        }

        verifyEmail(token)
            .then(() => {

                setSuccess(true);

            })
            .catch((err) => {

                setError(
                    err.response?.data?.detail ||
                    "Verification failed."
                );

            })
            .finally(() => {

                setLoading(false);

            });

    }, []);

    if (loading)
        return <h2>Verifying your email...</h2>;

    if (success)
        return (
            <div>

                <h1>Email Verified 🎉</h1>

                <p>
                    Your account has been verified.
                </p>

                <Link to="/login">
                    Go to Login
                </Link>

            </div>
        );

    return (

        <div>

            <h1>Verification Failed</h1>

            <p>{error}</p>

            <ResendVerification />

        </div>

    );

}