import { useRef, useState } from "react";
import { Upload, FileText } from "lucide-react";
import { toast } from "react-toastify";

import { uploadResume } from "../api/resumeApi";

function ResumeUpload({ refreshResume }) {
  const inputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSelect = (e) => {
    if (e.target.files.length === 0) return;

    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error("Please select a PDF file.");
      return;
    }

    if (file.type !== "application/pdf") {
      toast.error("Only PDF files are allowed.");
      return;
    }

    try {
      setLoading(true);

      await uploadResume(file);

      toast.success("Resume uploaded successfully.");

      setFile(null);

      if (inputRef.current) {
        inputRef.current.value = "";
      }

      refreshResume();
    } catch (err) {
      toast.error(
        err.response?.data?.detail || "Resume upload failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-xl border bg-white p-8 shadow-sm">

      <div className="flex flex-col items-center text-center">

        <Upload
          size={56}
          className="text-indigo-600"
        />

        <h2 className="mt-4 text-2xl font-semibold">
          Upload Resume
        </h2>

        <p className="mt-2 text-gray-500">
          Upload your latest resume in PDF format.
        </p>

        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          onChange={handleSelect}
          className="mt-6"
        />

        {file && (
          <div className="mt-5 flex items-center gap-2 rounded-lg bg-gray-100 px-4 py-2">
            <FileText
              size={18}
              className="text-indigo-600"
            />

            <span className="text-sm font-medium">
              {file.name}
            </span>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={loading}
          className="mt-6 rounded-lg bg-indigo-600 px-6 py-3 font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? "Uploading..." : "Upload Resume"}
        </button>

      </div>

    </div>
  );
}

export default ResumeUpload;