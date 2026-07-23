import { useSelector } from "react-redux";
import {
  FileText,
  Briefcase,
  Trophy,
} from "lucide-react";

import DashboardCard from "../layouts/DashboardCard";

function Dashboard() {
  const user = useSelector((state) => state.auth.user);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold">
          Welcome back, {user?.full_name} 👋
        </h1>

        <p className="mt-2 text-gray-500">
          Ready to ace your next interview?
        </p>
      </div>

      {/* Stats */}
      <div className="grid gap-6 md:grid-cols-3">
        <DashboardCard
          title="Resume"
          value="Uploaded"
          subtitle="1 Resume"
          icon={FileText}
          color="blue"
        />

        <DashboardCard
          title="Interviews"
          value="0"
          subtitle="Completed"
          icon={Briefcase}
          color="green"
        />

        <DashboardCard
          title="Average Score"
          value="--"
          subtitle="No interviews yet"
          icon={Trophy}
          color="purple"
        />
      </div>

      {/* Quick Actions */}
      <div className="rounded-xl bg-white p-6 shadow-sm border">
        <h2 className="text-xl font-semibold mb-4">
          Quick Actions
        </h2>

        <div className="flex flex-wrap gap-4">
          <button className="rounded-lg bg-blue-600 px-5 py-3 text-white hover:bg-blue-700 transition">
            Upload Resume
          </button>

          <button className="rounded-lg bg-green-600 px-5 py-3 text-white hover:bg-green-700 transition">
            Start Interview
          </button>
        </div>
      </div>

      {/* Recent Interviews */}
      <div className="rounded-xl bg-white p-6 shadow-sm border">
        <h2 className="text-xl font-semibold mb-4">
          Recent Interviews
        </h2>

        <p className="text-gray-500">
          No interviews found.
        </p>
      </div>
    </div>
  );
}

export default Dashboard;