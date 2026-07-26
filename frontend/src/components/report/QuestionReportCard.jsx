import { useState } from "react";
import {
    ChevronDown,
    ChevronRight,
    CheckCircle,
} from "lucide-react";

function QuestionReportCard({ report, index }) {
    const [expanded, setExpanded] = useState(index === 0);

    return (
        <div className="bg-white border rounded-xl shadow-sm overflow-hidden">

            <button
                onClick={() => setExpanded(!expanded)}
                className="w-full flex items-center justify-between px-6 py-4 hover:bg-gray-50"
            >
                <div className="text-left">
                    <h3 className="text-lg font-semibold">
                        Question {index + 1}
                    </h3>

                    <p className="text-sm text-gray-500 mt-1">
                        {report.topic} • {report.difficulty}
                    </p>
                </div>

                {expanded ? (
                    <ChevronDown />
                ) : (
                    <ChevronRight />
                )}
            </button>

            {expanded && (
                <div className="border-t px-6 py-6 space-y-6">

                    <section>
                        <h4 className="font-semibold mb-2">
                            Question
                        </h4>

                        <p className="text-gray-700">
                            {report.question}
                        </p>
                    </section>

                    <section>
                        <h4 className="font-semibold mb-2">
                            Your Answer
                        </h4>

                        <div className="rounded-lg bg-gray-50 p-4">
                            {report.candidate_answer}
                        </div>
                    </section>

                    <section>
                        <div className="flex items-center justify-between mb-2">
                            <h4 className="font-semibold">
                                AI Feedback
                            </h4>

                            <span className="font-bold text-indigo-600">
                                {report.score}/10
                            </span>
                        </div>

                        <div className="rounded-lg bg-yellow-50 border border-yellow-200 p-4">
                            {report.feedback}
                        </div>
                    </section>

                    <section>
                        <h4 className="font-semibold mb-2 text-green-700">
                            Ideal Answer
                        </h4>

                        <div className="rounded-lg bg-green-50 border border-green-200 p-4 whitespace-pre-line">
                            {report.ideal_answer}
                        </div>
                    </section>

                    <section>
                        <h4 className="font-semibold mb-3">
                            Key Learning Points
                        </h4>

                        <ul className="space-y-2">
                            {report.key_learning_points.map(
                                (point, idx) => (
                                    <li
                                        key={idx}
                                        className="flex items-start gap-2"
                                    >
                                        <CheckCircle
                                            size={18}
                                            className="text-green-600 mt-1"
                                        />

                                        <span>{point}</span>
                                    </li>
                                )
                            )}
                        </ul>
                    </section>

                </div>
            )}
        </div>
    );
}

export default QuestionReportCard;