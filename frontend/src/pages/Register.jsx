import { useForm } from "react-hook-form";
import { useNavigate, Link } from "react-router-dom";
import { toast } from "react-toastify";

import { register as registerUser } from "../api/authApi";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";

function Register() {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm();

  const password = watch("password");

  const onSubmit = async (data) => {
    try {
      await registerUser(data);

      toast.success("Registration successful!");

      navigate("/");
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Registration failed"
      );
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100">
      <div className="w-full max-w-md rounded-xl bg-white p-8 shadow-lg">

        <h1 className="mb-2 text-center text-3xl font-bold">
          Create Account
        </h1>

        <p className="mb-6 text-center text-gray-500">
          Welcome to InterviewIQ
        </p>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="space-y-4"
        >
          <Input
            label="Full Name"
            name="full_name"
            register={register}
            error={errors.full_name}
            rules={{
              required: "Full name is required",
            }}
          />

          <Input
            label="Email"
            type="email"
            name="email"
            register={register}
            error={errors.email}
            rules={{
              required: "Email is required",
            }}
          />

          <Input
            label="Password"
            type="password"
            name="password"
            register={register}
            error={errors.password}
            rules={{
              required: "Password is required",
              minLength: {
                value: 8,
                message:
                  "Password must be at least 8 characters",
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
              required: "Confirm your password",
              validate: (value) =>
                value === password ||
                "Passwords do not match",
            }}
          />

          <Button
            type="submit"
            loading={isSubmitting}
          >
            Register
          </Button>
        </form>

        <p className="mt-6 text-center text-sm">
          Already have an account?

          <Link
            to="/"
            className="ml-2 font-semibold text-blue-600"
          >
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Register;

