import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getInterviews } from "../api/interviewApi";

function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const interviews = await getInterviews();

        setReports(
          interviews.filter(
            (item) => item.status === "COMPLETED"
          )
        );
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-10">
        Loading...
      </div>
    );
  }

  if (reports.length === 0) {
    return (
      <div className="rounded-xl border bg-white p-8 text-center">
        <h2 className="text-xl font-semibold">
          No Reports Available
        </h2>

        <p className="mt-2 text-gray-500">
          Complete an interview to generate a report.
        </p>
      </div>
    );
  }

  return (
    <div>

      <h1 className="mb-6 text-3xl font-bold">
        Interview Reports
      </h1>

      <div className="grid gap-5">

        {reports.map((report) => (

          <div
            key={report.id}
            className="rounded-xl border bg-white p-6 shadow-sm"
          >

            <div className="flex justify-between items-start">

              <div>

                <h2 className="text-xl font-semibold">
                  {report.company_name}
                </h2>

                <p className="mt-1 text-gray-500">
                  {report.job_role}
                </p>

                <p className="mt-3 text-sm text-gray-400">
                  {new Date(
                    report.created_at
                  ).toLocaleDateString()}
                </p>

              </div>

              <span className="rounded-full bg-green-100 px-3 py-1 text-sm text-green-700">
                Completed
              </span>

            </div>

            <button
              onClick={() =>
                navigate(
                  `/interviews/${report.id}/report`
                )
              }
              className="mt-6 rounded-lg bg-indigo-600 px-5 py-2 text-white hover:bg-indigo-700"
            >
              View Report
            </button>

          </div>

        ))}

      </div>

    </div>
  );
}

export default Reports;