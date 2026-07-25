import { useState } from "react";
import { resendVerification } from "../../api/authApi";

export default function ResendVerification() {

    const [email, setEmail] = useState("");

    const [message, setMessage] = useState("");

    const submit = async (e) => {

        e.preventDefault();

        try {

            const response =
                await resendVerification(email);

            setMessage(response.message);

        }
        catch (err) {

            setMessage(
                err.response?.data?.detail ||
                "Unable to resend email."
            );

        }

    };

    return (

        <form onSubmit={submit}>

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) =>
                    setEmail(e.target.value)
                }
            />

            <button>

                Resend Verification

            </button>

            <p>{message}</p>

        </form>

    );

}