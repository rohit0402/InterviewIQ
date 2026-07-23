import { useState } from "react";
import { Upload } from "lucide-react";
import { toast } from "react-toastify";

import { uploadResume } from "../../api/resumeApi";

function ResumeUpload({ refreshResume }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      toast.error("Please select a PDF.");
      return;
    }

    try {
      setLoading(true);

      await uploadResume(file);

      toast.success("Resume uploaded successfully!");

      refreshResume();
    } catch (err) {
      toast.error(
        err.response?.data?.detail ??
          "Upload failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-xl border bg-white p-8 shadow-sm">

      <div className="flex flex-col items-center gap-5">

        <Upload
          className="text-blue-600"
          size={55}
        />

        <h2 className="text-xl font-semibold">
          Upload Resume
        </h2>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) =>
            setFile(e.target.files[0])
          }
        />

        {file && (
          <p className="text-gray-500">
            {file.name}
          </p>
        )}

        <button
          disabled={loading}
          onClick={handleUpload}
          className="rounded-lg bg-blue-600 px-6 py-3 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading
            ? "Uploading..."
            : "Upload Resume"}
        </button>
      </div>
    </div>
  );
}

export default ResumeUpload;