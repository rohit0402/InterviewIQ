import { configureStore } from "@reduxjs/toolkit";
import  authReducer  from "../features/auth/authSlice";
import resumeReducer from "../features/resume/resumeSlice";
import interviewReducer from "../features/interview/interviewSlice";

// configure store creates redux store and reducer creates global state which you can access anywhere like state.auth,state.resume

export const store = configureStore({
    reducer:{
        auth: authReducer,
        resume: resumeReducer,
        interview: interviewReducer 
    },
});