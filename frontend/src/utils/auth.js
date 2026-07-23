import { store } from "../app/store";
import { setCredentials, clearCredentials } from "../features/auth/authSlice";
import {getCurrentUser} from "../api/authApi";
import api from "../api/axios";

export const refreshToken = async () => {
    try{
        const response= await api.post("/auth/refresh");

        const accessToken=response.data.access_token;
        
        store.dispatch(setCredentials({user:store.getState().auth.user,accessToken}));
        return accessToken;
    }
    catch(error){
        store.dispatch(clearCredentials());
        throw error;
    }
};

export const logoutUser= async () =>{
    try{
        await api.post("/auth/logout");
    }catch(error){

    }
    store.dispatch(clearCredentials());
}