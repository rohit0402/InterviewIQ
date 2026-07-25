import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

import AuthCard from "../components/auth/AuthCard";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";

import { forgotPassword } from "../api/authApi";

function ForgotPasswordPage() {
    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm();

    const [emailSent, setEmailSent] = useState(false);

    const onSubmit = async (data) => {
        try {
            await forgotPassword(data.email);

            setEmailSent(true);

            toast.success("Password reset email sent.");
        } catch (error) {
            toast.error(
                error.response?.data?.detail ||
                "Something went wrong."
            );
        }
    };

    if (emailSent) {
        return (
            <AuthCard>
                <h1 className="mb-4 text-center text-3xl font-bold">
                    Check your email
                </h1>

                <p className="text-center text-gray-600">
                    If an account exists, we've sent a password reset link.
                </p>

                <Link
                    to="/"
                    className="mt-6 block text-center font-semibold text-blue-600"
                >
                    Back to Login
                </Link>
            </AuthCard>
        );
    }

    return (
        <AuthCard>
            <h1 className="mb-6 text-center text-3xl font-bold">
                Forgot Password
            </h1>

            <form onSubmit={handleSubmit(onSubmit)}>
                <Input
                    label="Email"
                    type="email"
                    name="email"
                    placeholder="Enter your email"
                    register={register}
                    error={errors.email}
                    rules={{
                        required: "Email is required",
                    }}
                />

                <Button
                    type="submit"
                    loading={isSubmitting}
                >
                    Send Reset Link
                </Button>
            </form>

            <Link
                to="/"
                className="mt-6 block text-center text-blue-600"
            >
                Back to Login
            </Link>
        </AuthCard>
    );
}

export default ForgotPasswordPage;