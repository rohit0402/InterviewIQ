import { store } from "../app/store";
import { setCredentials, clearCredentials } from "../features/auth/authSlice";
import {refresh} from "../api/authApi";

export const refreshToken = async () => {
    const auth=store.getState().auth;

    if(!auth.refreshToken){
        throw new Error("Refresh token not found");
    }
    const response=await refresh(auth.refreshToken);
    store.dispatch(
        setCredentials({
            user:auth.user,
            accessToken:response.access_token,
            refreshToken:auth.refreshToken,
        })
    );
    return response.accessToken;
};

export const logoutUser=  ()=>{
    store.dispatch(clearCredentials());
}