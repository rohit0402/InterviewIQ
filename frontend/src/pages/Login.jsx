import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { getCurrentUser } from "../api/authApi";
import { login } from "../api/authApi";
import { setCredentials } from "../features/auth/authSlice";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";
import { Link } from "react-router-dom";
import AuthCard from "../components/auth/AuthCard.jsx";

function Login() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      // Login
      const response = await login(data);

      // Save tokens first
      dispatch(
        setCredentials({
          user: null,
          accessToken: response.access_token,
        }),
      );

      // Fetch logged-in user
      const user = await getCurrentUser();

      // Update Redux with user
      dispatch(
        setCredentials({
          user,
          accessToken: response.access_token,
        }),
      );

      toast.success("Login successful!");

      navigate("/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Login failed");
    }
  };

  return (
    <AuthCard>
      <h1 className="mb-6 text-center text-3xl font-bold">Welcome Back</h1>

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

        <Input
          label="Password"
          type="password"
          name="password"
          placeholder="Enter your password"
          register={register}
          error={errors.password}
          rules={{
            required: "Password is required",
          }}
        />
        <div className="mb-4 text-right">
          <Link
            to="/forgot-password"
            className="text-sm text-blue-600 hover:underline"
          >
            Forgot Password?
          </Link>
        </div>
        <Button type="submit" loading={isSubmitting}>
          Login
        </Button>
      </form>
      <p className="mt-6 text-center text-sm">
        New User?
        <Link to="/register" className="ml-2 font-semibold text-blue-600">
          Register
        </Link>
      </p>
    </AuthCard>
  );
}

export default Login;
