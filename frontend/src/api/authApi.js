import api from "./axios";

export const register = async (data) => {
  const response = await api.post("/auth/register", data);
  return response.data;
};

export const login = async (data) => {
  const response = await api.post("/auth/login", data);
  return response.data;
};

export const refresh = async () => {
  const response = await api.post("/auth/refresh");

  return response.data;
};

export const logout = async () => {
  const response = await api.post("/auth/logout");

  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get("/users/me");
  return response.data;
};

export const changePassword = async (data) => {
  const response = await api.post("/users/change-password", data);
  return response.data;
};

export const verifyEmail = async (token) => {
    const response = await api.get(
        `/auth/verify-email`,
        {
            params: {
                token,
            },
        }
    );

    return response.data;
};

export const resendVerification = async (email) => {
    const response = await api.post(
        "/auth/resend-verification",
        {
            email,
        }
    );

    return response.data;
};
export const forgotPassword = async (email) => {
  const response = await api.post("/auth/forgot-password", {
    email,
  });

  return response.data;
};

export const resetPassword = async (token, password) => {
  const response = await api.post("/auth/reset-password", {
    token,
    password,
  });

  return response.data;
};