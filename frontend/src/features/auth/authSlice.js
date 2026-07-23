import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    user: null,
    accessToken: null,
    isAuthenticated: false,
    loading: false,
};

const authSlice=createSlice({
    name:"auth",
    initialState,
    reducers:{
        setCredentials:(state,acion)=>{
            state.user=acion.payload.user;
            state.accessToken=acion.payload.accessToken;
            state.isAuthenticated=true;
        },
        clearCredentials:(state)=>{
            state.user=null;
            state.accessToken=null;
            state.isAuthenticated=false;
        },
        setLoading:(state,action)=>{
            state.loading=action.payload;
        },
    },
});

export const {setCredentials,clearCredentials,setLoading}=authSlice.actions;
export default authSlice.reducer;