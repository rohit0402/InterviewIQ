import { useEffect, useState } from "react";
import { getResume } from "../api/resumeApi";

import ResumeUpload from "../components/resume/ResumeUpload";
import ResumeCard from "../components/resume/ResumeCard";

function Resume() {
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchResume = async () => {
    try {
      const data = await getResume();
      setResume(data);
    } catch {
      setResume(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResume();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-10">
        Loading...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">
          Resume
        </h1>

        <p className="text-gray-500 mt-1">
          Upload your latest resume for AI analysis.
        </p>
      </div>

      {resume ? (
        <ResumeCard
          resume={resume}
          refreshResume={fetchResume}
        />
      ) : (
        <ResumeUpload
          refreshResume={fetchResume}
        />
      )}
    </div>
  );
}

export default Resume;