import { useState } from "react";

const initialForm = {
    company_name: "",
    job_role: "",
    experience_level: "Fresher",
    job_description: "",
};

function InterviewForm({ onCreate, loading }) {
    const [formData, setFormData] = useState(initialForm);

    const handleChange = (e) => {
        setFormData((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (
            !formData.company_name.trim() ||
            !formData.job_role.trim() ||
            !formData.job_description.trim()
        ) {
            alert("Please fill all required fields.");
            return;
        }

        await onCreate(formData);

        setFormData(initialForm);
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white rounded-xl border shadow-sm p-6 space-y-5"
        >
            <h2 className="text-2xl font-semibold">
                Create Interview
            </h2>

            <div>
                <label className="block mb-2 font-medium">
                    Company Name
                </label>

                <input
                    type="text"
                    name="company_name"
                    value={formData.company_name}
                    onChange={handleChange}
                    placeholder="Google"
                    className="w-full border rounded-lg p-3"
                />
            </div>

            <div>
                <label className="block mb-2 font-medium">
                    Job Role
                </label>

                <input
                    type="text"
                    name="job_role"
                    value={formData.job_role}
                    onChange={handleChange}
                    placeholder="Software Engineer"
                    className="w-full border rounded-lg p-3"
                />
            </div>

            <div>
                <label className="block mb-2 font-medium">
                    Experience Level
                </label>

                <select
                    name="experience_level"
                    value={formData.experience_level}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3"
                >
                    <option>Fresher</option>
                    <option>0-2 Years</option>
                    <option>2-5 Years</option>
                    <option>5+ Years</option>
                </select>
            </div>

            <div>
                <label className="block mb-2 font-medium">
                    Job Description
                </label>

                <textarea
                    rows={8}
                    name="job_description"
                    value={formData.job_description}
                    onChange={handleChange}
                    placeholder="Paste the complete job description..."
                    className="w-full border rounded-lg p-3 resize-none"
                />
            </div>

            <button
                disabled={loading}
                className="w-full py-3 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
            >
                {loading
                    ? "Creating..."
                    : "Create Interview"}
            </button>
        </form>
    );
}

export default InterviewForm;