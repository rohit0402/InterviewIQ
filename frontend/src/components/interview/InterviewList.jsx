import InterviewCard from "./InterviewCard";

function InterviewList({ interviews, onDelete }) {
  if (interviews.length === 0) {
    return (
      <div className="bg-white rounded-xl border p-8 text-center text-gray-500">
        No interviews created yet.
      </div>
    );
  }

  return (
    <div className="grid gap-5">
      {interviews.map((interview) => (
        <InterviewCard
          key={interview.id}
          interview={interview}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}

export default InterviewList;
