import api from "./axios";

export const startInterview = async (interviewId) => {
    const { data } = await api.post(`/interviews/${interviewId}/start`);
    return data;
};

export const submitAnswer = async (questionId, answer) => {
    const { data } = await api.post(
        `/interviews/question/${questionId}/answer`,
        {
            answer,
        }
    );

    return data;
};

export const nextQuestion = async (interviewId) => {
    const { data } = await api.post(
        `/interviews/${interviewId}/next-question`
    );

    return data;
};

export const finishInterview = async (interviewId) => {
    const { data } = await api.post(
        `/interviews/${interviewId}/finish`
    );

    return data;
};

// Add later after backend endpoint exists
export const getInterviewReport = async (interviewId) => {
    const { data } = await api.get(
        `/interviews/${interviewId}/report`
    );

    return data;
};

export const createInterview = async (payload) => {
    const { data } = await api.post("/interviews", payload);
    return data;
};

export const getInterviews = async () => {
    const { data } = await api.get("/interviews/");
    return data;
};

export const deleteInterview = async (interviewId) => {
    await api.delete(`/interviews/${interviewId}`);
};