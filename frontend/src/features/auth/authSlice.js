import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    user: null,
    accessToken: null,
    isAuthenticated: false,
    loading: false,
    initialized: false,
};

const authSlice=createSlice({
    name:"auth",
    initialState,
    reducers:{
        setCredentials: (state, action) => {
    state.user = action.payload.user;
    state.accessToken = action.payload.accessToken;
    state.isAuthenticated = true;
    state.initialized = true;
},
        clearCredentials: (state) => {
    state.user = null;
    state.accessToken = null;
    state.isAuthenticated = false;
    state.initialized = true;
},
        setLoading:(state,action)=>{
            state.loading=action.payload;
        },
        setInitialized: (state) => {
    state.initialized = true;
},
    },
});

export const {setCredentials,clearCredentials,setLoading,setInitialized} = authSlice.actions;
export default authSlice.reducer;