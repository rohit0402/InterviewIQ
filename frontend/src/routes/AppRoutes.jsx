import { BrowserRouter, Routes, Route } from "react-router-dom";

import InterviewSession from "../pages/InterviewSession";
import InterviewReport from "../pages/InterviewReport";
import ProtectedRoute from "../components/ProtectedRoute";
import DashboardLayout from "../layouts/DashboardLayout";
import ResumeAnalysis from "../pages/ResumeAnalysis";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import Resume from "../pages/Resume";
import Interviews from "../pages/Interview";
import Reports from "../pages/Reports";
import Profile from "../pages/Profile";
import ForgotPasswordPage from "../pages/ForgotPasswordPage";
import ResetPasswordPage from "../pages/ResetPasswordPage";
import VerifyEmail from "../pages/VerifyEmail";
function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        <Route path="/verify-email" element={<VerifyEmail />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />

        <Route path="/reset-password" element={<ResetPasswordPage />} />
        {/* Protected Routes */}
        <Route element={<ProtectedRoute />}>
          <Route element={<DashboardLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/resume" element={<Resume />} />
            <Route path="/resume/analysis" element={<ResumeAnalysis />} />
            <Route path="/interviews" element={<Interviews />} />
            <Route
              path="/interviews/:id/session"
              element={<InterviewSession />}
            />
            <Route
              path="/interv
              iews/:id/report"
              element={<InterviewReport />}
            />
            <Route path="/reports" element={<Reports />} />
            <Route path="/profile" element={<Profile />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
