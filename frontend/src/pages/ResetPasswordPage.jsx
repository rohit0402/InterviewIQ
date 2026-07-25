import { useForm } from "react-hook-form";
import { useNavigate, useSearchParams } from "react-router-dom";
import { toast } from "react-toastify";

import AuthCard from "../components/auth/AuthCard";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";

import { resetPassword } from "../api/authApi";

function ResetPasswordPage() {

    const navigate = useNavigate();

    const [params] = useSearchParams();

    const token = params.get("token");

    const {
        register,
        handleSubmit,
        watch,
        formState: { errors, isSubmitting },
    } = useForm();

    const onSubmit = async (data) => {

        if (data.password !== data.confirmPassword) {
            toast.error("Passwords do not match.");
            return;
        }

        try {

            await resetPassword(
                token,
                data.password
            );

            toast.success("Password updated successfully.");

            navigate("/");

        } catch (error) {

            toast.error(
                error.response?.data?.detail ||
                "Unable to reset password."
            );

        }
    };

    return (
        <AuthCard>

            <h1 className="mb-6 text-center text-3xl font-bold">
                Reset Password
            </h1>

            <form onSubmit={handleSubmit(onSubmit)}>

                <Input
                    label="New Password"
                    type="password"
                    name="password"
                    register={register}
                    error={errors.password}
                    rules={{
                        required: "Password is required",
                        minLength: {
                            value: 8,
                            message:
                                "Minimum 8 characters",
                        },
                    }}
                />

                <Input
                    label="Confirm Password"
                    type="password"
                    name="confirmPassword"
                    register={register}
                    error={errors.confirmPassword}
                    rules={{
                        required:
                            "Please confirm password",
                        validate: value =>
                            value === watch("password") ||
                            "Passwords do not match",
                    }}
                />

                <Button
                    type="submit"
                    loading={isSubmitting}
                >
                    Reset Password
                </Button>

            </form>

        </AuthCard>
    );
}

export default ResetPasswordPage;