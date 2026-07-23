import { Trash2, Eye } from "lucide-react";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

import { deleteResume } from "../../api/resumeApi";

function ResumeCard({
  resume,
  refreshResume,
}) {
  const navigate = useNavigate();

  const handleDelete = async () => {
    if (
      !window.confirm(
        "Delete this resume?"
      )
    )
      return;

    try {
      await deleteResume();

      toast.success("Resume deleted.");

      refreshResume();
    } catch (err) {
      toast.error(
        err.response?.data?.detail ??
          "Delete failed"
      );
    }
  };

  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm">

      <h2 className="text-xl font-semibold">
        {resume.original_filename}
      </h2>

      <div className="mt-4 space-y-2">

        <p>
          <strong>Status:</strong>{" "}
          {resume.status}
        </p>

        <p>
          <strong>Uploaded:</strong>{" "}
          {new Date(
            resume.created_at
          ).toLocaleDateString()}
        </p>

        <p>
          <strong>Size:</strong>{" "}
          {(resume.file_size / 1024).toFixed(2)}
          {" KB"}
        </p>

      </div>

      <div className="mt-6 flex gap-4">

        {resume.analysis_available && (
          <button
            onClick={() =>
              navigate("/resume/analysis")
            }
            className="flex items-center gap-2 rounded-lg bg-green-600 px-4 py-2 text-white"
          >
            <Eye size={18} />

            View Analysis
          </button>
        )}

        <button
          onClick={handleDelete}
          className="flex items-center gap-2 rounded-lg bg-red-600 px-4 py-2 text-white"
        >
          <Trash2 size={18} />

          Delete
        </button>

      </div>

    </div>
  );
}

export default ResumeCard;