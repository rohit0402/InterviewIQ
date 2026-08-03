import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { FileText, Briefcase, Trophy, ArrowRight, Eye } from "lucide-react";

import DashboardCard from "../layouts/DashboardCard";
import { getDashboard } from "../api/dashboardApi";

function Dashboard() {
  const user = useSelector((state) => state.auth.user);
  const navigate = useNavigate();

  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await getDashboard();
      setDashboard(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-20">Loading Dashboard...</div>
    );
  }

  if (!dashboard) {
    return <div>Loading...</div>;
  } else {
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
            value={dashboard.resume_uploaded ? "Uploaded" : "Not Uploaded"}
            subtitle="Resume Status"
            icon={FileText}
            color="blue"
          />

          <DashboardCard
            title="Interviews"
            value={dashboard.total_interviews}
            subtitle={`${dashboard.completed_interviews} Completed`}
            icon={Briefcase}
            color="green"
          />

          {/* <DashboardCard
          title="Average Score"
          value={
    dashboard.average_score
        ? `${dashboard.average_score.toFixed(1)}/10`
        : "--"
}
          subtitle="Overall"
          icon={Trophy}
          color="purple"
        /> */}
        </div>

        {/* Quick Actions */}

        <div className="rounded-xl bg-white p-6 shadow-sm border">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>

          <div className="flex flex-wrap gap-4">
            <button
              onClick={() => navigate("/resume")}
              className="rounded-lg bg-blue-600 px-5 py-3 text-white hover:bg-blue-700"
            >
              Resume
            </button>

            <button
              onClick={() => navigate("/interviews")}
              className="rounded-lg bg-green-600 px-5 py-3 text-white hover:bg-green-700"
            >
              Interviews
            </button>
          </div>
        </div>

        {/* Recent Interviews */}

        {/* Recent Interviews */}

        <div className="rounded-xl bg-white p-6 shadow-sm border">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Recent Interviews</h2>

            <button
              onClick={() => navigate("/reports")}
              className="text-indigo-600 hover:text-indigo-700 font-medium"
            >
              View All →
            </button>
          </div>

          {dashboard.recent_interviews.length === 0 ? (
            <div className="text-center py-10">
              <p className="text-gray-500">
                You haven't taken any interviews yet.
              </p>

              <button
                onClick={() => navigate("/interviews")}
                className="mt-4 bg-indigo-600 text-white px-5 py-2 rounded-lg hover:bg-indigo-700"
              >
                Start Interview
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {dashboard.recent_interviews.map((item) => (
                <div
                  key={item.id}
                  className="border rounded-xl p-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4 hover:shadow-sm transition"
                >
                  <div>
                    <h3 className="text-lg font-semibold">
                      {item.company_name}
                    </h3>

                    <p className="text-gray-500">{item.job_role}</p>

                    <span
  className={`inline-block mt-3 px-3 py-1 rounded-full text-sm font-medium ${
    item.status === "REPORT_READY"
      ? "bg-green-100 text-green-700"
      : "bg-yellow-100 text-yellow-700"
  }`}
>
  {item.status.replace(/_/g, " ")}
</span>
                  </div>

                  <div className="flex items-center gap-5">
                    {item.overall_score !== null && (
                      <div className="text-center">
                        <p className="text-sm text-gray-500">Score</p>

                        <p className="text-2xl font-bold text-indigo-600">
                          {item.overall_score.toFixed(1)}
                          /10
                        </p>
                      </div>
                    )}

                    {item.status === "REPORT_READY" ? (
                      <button
                        onClick={() =>
                          navigate(`/interviews/${item.id}/report`)
                        }
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-lg"
                      >
                        View Report
                      </button>
                    ) : (
                      <button
                        onClick={() =>
                          navigate(`/interviews/${item.id}/session`)
                        }
                        className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-lg"
                      >
                        Continue
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }
}

export default Dashboard;
