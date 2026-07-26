import { useEffect, useState } from "react";
import {
  createInterview,
  deleteInterview,
  getInterviews,
} from "../api/interviewApi";
import InterviewForm from "../components/interview/InterviewForm";
import InterviewList from "../components/interview/InterviewList";
import { useNavigate } from "react-router-dom";

function Interviews() {
  const navigate = useNavigate();
  const [interviews, setInterviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const handleDelete = async (interviewId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this interview?",
    );

    if (!confirmed) return;

    try {
      await deleteInterview(interviewId);

      setInterviews((prev) =>
        prev.filter((interview) => interview.id !== interviewId),
      );
    } catch (error) {
      console.error(error);
    }
  };
  const loadInterviews = async () => {
    try {
      const data = await getInterviews();
      setInterviews(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadInterviews();
  }, []);

  const handleCreateInterview = async (formData) => {
  try {
    setLoading(true);

    const interview = await createInterview(formData);

    console.log(interview);

    navigate(`/interviews/${interview.id}/session`);
  } catch (error) {
    console.error(error);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="max-w-7xl mx-auto py-8 grid lg:grid-cols-2 gap-8">
      <InterviewForm onCreate={handleCreateInterview} loading={loading} />

      <InterviewList interviews={interviews} onDelete={handleDelete} />
    </div>
  );
}

export default Interviews;
