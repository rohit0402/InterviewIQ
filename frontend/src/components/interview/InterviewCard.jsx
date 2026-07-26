import { useNavigate } from "react-router-dom";
import { Play, ArrowRight, Eye, Trash2 } from "lucide-react";

function InterviewCard({ interview, onDelete }) {
    const navigate = useNavigate();

    const renderActionButton = () => {
        switch (interview.status) {

            case "PENDING":
            case "NOT_STARTED":
                return (
                    <button
                        onClick={() =>
                            navigate(`/interviews/${interview.id}/session`)
                        }
                        className="flex-1 flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700 transition"
                    >
                        <Play size={18} />
                        Start Interview
                    </button>
                );

            case "IN_PROGRESS":
                return (
                    <button
                        onClick={() =>
                            navigate(`/interviews/${interview.id}/session`)
                        }
                        className="flex-1 flex items-center justify-center gap-2 rounded-lg bg-yellow-600 px-4 py-2 text-white hover:bg-yellow-700 transition"
                    >
                        <ArrowRight size={18} />
                        Continue
                    </button>
                );

            case "COMPLETED":
                return (
                    <button
                        onClick={() =>
                            navigate(`/interviews/${interview.id}/report`)
                        }
                        className="flex-1 flex items-center justify-center gap-2 rounded-lg bg-green-600 px-4 py-2 text-white hover:bg-green-700 transition"
                    >
                        <Eye size={18} />
                        View Report
                    </button>
                );

            default:
                return null;
        }
    };

    const statusColor = {
        PENDING: "bg-gray-100 text-gray-700",
        NOT_STARTED: "bg-gray-100 text-gray-700",
        IN_PROGRESS: "bg-yellow-100 text-yellow-700",
        COMPLETED: "bg-green-100 text-green-700",
    };

    return (
        <div className="rounded-xl border bg-white p-6 shadow-sm hover:shadow-md transition">

            <div className="flex justify-between items-start">

                <div>

                    <h2 className="text-xl font-semibold">
                        {interview.company_name}
                    </h2>

                    <p className="mt-1 text-gray-500">
                        {interview.job_role}
                    </p>

                </div>

                <span
                    className={`rounded-full px-3 py-1 text-sm font-medium ${
                        statusColor[interview.status] ??
                        "bg-gray-100 text-gray-700"
                    }`}
                >
                    {interview.status.replace("_", " ")}
                </span>

            </div>

            {interview.status === "COMPLETED" &&
                interview.overall_score != null && (

                    <div className="mt-5 rounded-lg bg-indigo-50 p-4">

                        <p className="text-sm text-gray-500">
                            Overall Score
                        </p>

                        <p className="text-3xl font-bold text-indigo-600">
                            {interview.overall_score.toFixed(1)}/10
                        </p>

                    </div>

                )}

            <div className="mt-6 flex gap-3">

                {renderActionButton()}

                <button
                    onClick={() => onDelete(interview.id)}
                    className="flex items-center justify-center gap-2 rounded-lg bg-red-600 px-4 py-2 text-white hover:bg-red-700 transition"
                >
                    <Trash2 size={18} />
                    Delete
                </button>

            </div>

        </div>
    );
}

export default InterviewCard;