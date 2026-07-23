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