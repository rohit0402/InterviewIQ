import {createSlice} from "@reduxjs/toolkit";

const initialState={
    resume:null,
    analysis:null,
    loading:false
}

const resumeSlice=createSlice({ 
    name:"resume",
    initialState,
    reducers:{
        setResume:(state,action)=>{
            state.resume=action.payload;
        },
        setAnalysis:(state,action)=>{
            state.analysis=action.payload;
        },
        clearResume:(state)=>{
            state.resume=null;
            state.analysis=null;
        },
        setLoading:(state,action)=>{
            state.loading=action.payload;
        },
    },
});

export const {setResume,setAnalysis,clearResume,setLoading}=resumeSlice.actions;
export default resumeSlice.reducer;