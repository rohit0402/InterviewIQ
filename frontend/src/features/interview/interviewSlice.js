import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    interview: null,
    currentQuestion: null,
    history: [],
    report: null,
    loading: false,
};

const interviewSlice = createSlice({
    name: "interview",
    initialState,
    reducers:{
        setInterview: (state, action) => {
            state.interview = action.payload;
        },
        setCurrentQuestion: (state, action) => {
            state.currentQuestion = action.payload;
        },
        addHistory: (state, action) => {
            state.history.push(action.payload);
        },
        setReport: (state, action) => {
            state.report = action.payload;
        },
        clearInterview: (state) => {
            state.interview = null;
            state.currentQuestion = null;
            state.history = [];
            state.report = null;
        },
        setLoading: (state, action) => {
            state.loading = action.payload;
        },
    },
});

export const { setInterview, setCurrentQuestion, addHistory, setReport, clearInterview, setLoading } = interviewSlice.actions;

export default interviewSlice.reducer;