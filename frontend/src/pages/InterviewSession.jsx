import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import {
    startInterview,
    submitAnswer,
    nextQuestion,
    finishInterview,
} from "../api/interviewApi";

import QuestionCard from "../components/interview/QuestionCard";
import AnswerForm from "../components/interview/AnswerForm";
import ProgressBar from "../components/interview/ProgressBar";
import InterviewFeedback from "../components/interview/InterviewFeedback";

function InterviewSession() {
    const { id } = useParams();

    const [question, setQuestion] = useState(null);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [feedback, setFeedback] = useState(null);

    useEffect(() => {
        loadFirstQuestion();
    }, []);

    const loadFirstQuestion = async () => {
        try {
            const data = await startInterview(id);
            setQuestion(data);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (answer) => {
        try {
            setSubmitting(true);

            const result = await submitAnswer(
                question.id,
                answer
            );

            setFeedback(result);

        } finally {
            setSubmitting(false);
        }
    };

    const handleNext = async () => {
        try {
            const next = await nextQuestion(id);

            setQuestion(next);
            setFeedback(null);

        } catch {
            await finishInterview(id);

            // navigate to report
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="space-y-6">

            <ProgressBar
                sequence={question.sequence}
            />

            <QuestionCard
                question={question}
            />

            <AnswerForm
                loading={submitting}
                onSubmit={handleSubmit}
            />

            {feedback && (
                <InterviewFeedback
                    feedback={feedback}
                    onNext={handleNext}
                />
            )}

        </div>
    );
}

export default InterviewSession;