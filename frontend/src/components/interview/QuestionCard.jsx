function QuestionCard({ question }) {
    return (
        <div className="bg-white border rounded-xl shadow-sm p-6">
            <div className="flex justify-between mb-5">

                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                    {question.topic}
                </span>

                <span className="px-3 py-1 bg-gray-100 rounded-full text-sm">
                    {question.difficulty}
                </span>

            </div>

            <h2 className="text-xl font-semibold leading-relaxed">
                {question.question}
            </h2>
        </div>
    );
}

export default QuestionCard;