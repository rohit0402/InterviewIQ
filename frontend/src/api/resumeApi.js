import api from "./axios";

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const { data } = await api.post("/resumes/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return data;
};

export const getResume = async () => {
  const { data } = await api.get("/resumes");
  return data;
};


export const getResumeAnalysis = async () => {
    const { data } = await api.get("/resumes/analysis");
    return data;
};

export const deleteResume = async () => {
  await api.delete("/resumes");
};
