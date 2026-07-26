import { CheckCircle } from "lucide-react";

function InterviewFeedback({
  feedback,
  loading,
  onNext,
  onFinish,
}) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm">

      <div className="flex items-center gap-3">

        <CheckCircle
          className="text-green-600"
          size={28}
        />

        <div>
          <h2 className="text-xl font-semibold">
            Answer Submitted Successfully
          </h2>

          <p className="text-gray-500">
            Review your feedback and continue.
          </p>
        </div>

      </div>

      <div className="mt-6 rounded-lg bg-gray-50 p-4">

        <p className="font-medium">
          Score
        </p>

        <p className="mt-1 text-3xl font-bold text-indigo-600">
          {feedback.score.toFixed(1)} / 10
        </p>

      </div>

      <div className="mt-6">

        <h3 className="font-semibold">
          AI Feedback
        </h3>

        <p className="mt-2 whitespace-pre-wrap text-gray-700">
          {feedback.feedback}
        </p>

      </div>

      <div className="mt-8 flex gap-4">

        <button
          onClick={onNext}
          disabled={loading}
          className="flex-1 rounded-lg bg-indigo-600 py-3 font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading
            ? "Generating..."
            : "Next Question"}
        </button>

        <button
          onClick={onFinish}
          disabled={loading}
          className="flex-1 rounded-lg bg-green-600 py-3 font-medium text-white hover:bg-green-700 disabled:opacity-50"
        >
          Finish Interview
        </button>

      </div>

    </div>
  );
}

export default InterviewFeedback;