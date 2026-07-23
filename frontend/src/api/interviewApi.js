export const getInterviewReport = async (id) => {
    const { data } = await api.get(`/interviews/${id}/report`);
    return data;
};