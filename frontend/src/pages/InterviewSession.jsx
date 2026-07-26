import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import {
    finishInterview,
    nextQuestion,
    startInterview,
    submitAnswer,
} from "../api/interviewApi";

import ProgressBar from "../components/interview/ProgressBar";
import QuestionCard from "../components/interview/QuestionCard";
import AnswerForm from "../components/interview/AnswerForm";
import { set } from "react-hook-form";
// import InterviewFeedback from "../components/interview/InterviewFeedback";

function InterviewSession() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [answerSubmitted, setAnswerSubmitted] = useState(false);
    const [question, setQuestion] = useState(null);
    // const [feedback, setFeedback] = useState(null);

    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [nextLoading, setNextLoading] = useState(false);
    const handleFinishInterview = async () => {
        try {
            setNextLoading(true);

            const report = await finishInterview(id);

            navigate(
                `/interviews/${id}/report`,
                {
                    state: report,
                }
            );
        } catch (error) {
            console.error(error);
        } finally {
            setNextLoading(false);
        }
    };
    useEffect(() => {
        loadFirstQuestion();
    }, []);

    const loadFirstQuestion = async () => {
        try {
            setLoading(true);

            const data = await startInterview(id);

            setQuestion(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (answer) => {
        try {
            setSubmitting(true);

            const response = await submitAnswer(
                question.id,
                answer
            );

            toast.success(response.message);

            setAnswerSubmitted(true);
        } catch (error) {
            console.error(error);
        } finally {
            setSubmitting(false);
        }
    };

    const handleNextQuestion = async () => {
        try {
            setNextLoading(true);

            const next = await nextQuestion(id);

            setQuestion(next);
            // setFeedback(null);
        } catch (error) {
            try {
                const report = await finishInterview(id);

                navigate(
                    `/interviews/${id}/report`,
                    {
                        state: report,
                    }
                );
            } catch (finishError) {
                console.error(finishError);
            }
        } finally {
            setNextLoading(false);
            setAnswerSubmitted(false);
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center py-20">
                Preparing Interview...
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto py-8 space-y-6">

            <ProgressBar
                sequence={question.sequence}
            />

            <QuestionCard
                question={question}
            />

            {!answerSubmitted && (
                <AnswerForm
                    loading={submitting}
                    onSubmit={handleSubmit}
                />
            )}
            <div className="flex justify-end gap-4">
                <button
                    onClick={handleFinishInterview}
                    disabled={nextLoading}
                    className="px-6 py-2 rounded-lg border border-gray-300"
                >
                    Finish Interview
                </button>

                <button
                    onClick={handleNextQuestion}
                    disabled={!answerSubmitted || nextLoading}
                    className={`px-6 py-2 rounded-lg text-white ${answerSubmitted
                            ? "bg-indigo-600 hover:bg-indigo-700"
                            : "bg-gray-400 cursor-not-allowed"
                        }`}
                >
                    Next Question
                </button>
            </div>
        </div>
    );
}

export default InterviewSession;