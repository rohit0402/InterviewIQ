import { useState } from "react";

function AnswerForm({ onSubmit, loading }) {
    const [answer, setAnswer] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!answer.trim()) {
            alert("Answer cannot be empty.");
            return;
        }

        await onSubmit(answer);

        setAnswer("");
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white border rounded-xl shadow-sm p-6 space-y-4"
        >
            <textarea
                rows={8}
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Write your answer..."
                className="w-full border rounded-lg p-4 resize-none"
            />

            <button
                disabled={loading}
                className="w-full bg-indigo-600 text-white rounded-lg py-3 hover:bg-indigo-700 disabled:opacity-50"
            >
                {loading ? "Submitting..." : "Submit Answer"}
            </button>
        </form>
    );
}

export default AnswerForm;