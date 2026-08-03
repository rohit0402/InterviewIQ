import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";

import { getInterviewReport } from "../api/interviewApi";
import QuestionReportCard from "../components/report/QuestionReportCard";
function ScoreCard({ title, score }) {
  const scoreColor =
    score >= 8
      ? "text-green-600"
      : score >= 6
        ? "text-yellow-600"
        : "text-red-600";
  return (
    <div className="bg-white border rounded-xl shadow-sm p-5 text-center">
      <h3 className="text-gray-500 text-sm">{title}</h3>

      <p className={`text-4xl font-bold mt-2 ${scoreColor}`}>
        {Number(score).toFixed(1)}/10
      </p>
    </div>
  );
}

function InterviewReport() {
  const { id } = useParams();
  const location = useLocation();

  const [report, setReport] = useState(location.state || null);
  const [loading, setLoading] = useState(!location.state);
  const [error, setError] = useState("");

useEffect(() => {
  let cancelled = false;

  const loadReport = async () => {
    while (!cancelled) {
      try {
        const data = await getInterviewReport(id);

        if (!cancelled) {
          setReport(data);
          setLoading(false);
        }

        return;
      } catch (err) {
        if (err.response?.status === 202) {
          await new Promise((resolve) => setTimeout(resolve, 2000));
          continue;
        }

        if (!cancelled) {
          setError("Unable to load interview report.");
          setLoading(false);
        }

        return;
      }
    }
  };

  loadReport();

  return () => {
    cancelled = true;
  };
}, [id]);

  if (loading) {
    return (
      <div className="flex justify-center py-20 text-lg">Loading Report...</div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center py-20 text-red-600">{error}</div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-10 space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold">Interview Report</h1>

        <p className="text-gray-500 mt-2">AI Evaluation Summary</p>
      </div>

      <div className="grid md:grid-cols-4 gap-5">
        <ScoreCard title="Overall" score={report.overall_score} />

        <ScoreCard title="Communication" score={report.communication_score} />

        <ScoreCard title="Technical" score={report.technical_score} />

        <ScoreCard
          title="Problem Solving"
          score={report.problem_solving_score}
        />
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="bg-white border rounded-xl shadow-sm p-6">
          <h2 className="text-xl font-semibold text-green-600 mb-4">
            Strengths
          </h2>

          <ul className="space-y-2 list-disc list-inside">
            {report.strengths.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="bg-white border rounded-xl shadow-sm p-6">
          <h2 className="text-xl font-semibold text-red-600 mb-4">
            Weaknesses
          </h2>

          <ul className="space-y-2 list-disc list-inside">
            {report.weaknesses.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="bg-white border rounded-xl shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-3">Summary</h2>

        <p className="leading-8 text-gray-700">{report.summary}</p>
      </div>

      <div className="bg-white border rounded-xl shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-3">Hiring Recommendation</h2>

        <p className="leading-8 text-gray-700">
          {report.hiring_recommendation}
        </p>
      </div>

      <div className="bg-white border rounded-xl shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Improvement Plan</h2>

        <ol className="list-decimal list-inside space-y-3">
          {report.improvement_plan.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ol>
      </div>
      <div className="space-y-5">
        <div>
          <h2 className="text-3xl font-bold">Question Analysis</h2>

          <p className="text-gray-500 mt-1">
            Review every answer along with AI feedback and ideal responses.
          </p>
        </div>

        {report.question_reports?.length > 0 ? (
          report.question_reports.map((questionReport, index) => (
            <QuestionReportCard
              key={index}
              report={questionReport}
              index={index}
            />
          ))
        ) : (
          <div className="bg-white border rounded-xl p-6 text-center text-gray-500">
            No question analysis available.
          </div>
        )}
      </div>
    </div>
  );
}

export default InterviewReport;
