import { useEffect, useState } from "react";
import { getResumeAnalysis } from "../api/resumeApi";
import Section from "../components/analysis/Section";
import ListSection from "../components/analysis/ListSection";
import EducationSection from "../components/analysis/EducationSection";
import ExperienceSection from "../components/analysis/ExperienceSection";
import ProjectsSection from "../components/analysis/ProjectSection";

function ResumeAnalysis() {
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnalysis = async () => {
            try {
                const data = await getResumeAnalysis();
                setAnalysis(data);
            } finally {
                setLoading(false);
            }
        };

        fetchAnalysis();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!analysis) {
        return <div>No analysis found.</div>;
    }

    return (
        <div className="space-y-6">

            <div>
                <h1 className="text-3xl font-bold">
                    Resume Analysis
                </h1>

                <p className="text-gray-500">
                    AI generated analysis of your resume.
                </p>
            </div>

            <div className="rounded-xl bg-white p-6 shadow">
                <h2 className="font-semibold text-lg">
                    ATS Score
                </h2>

                <p className="text-5xl font-bold text-green-600 mt-3">
                    {analysis.ats_score}
                </p>
            </div>

            <Section
                title="Summary"
                content={analysis.summary}
            />

            <ListSection
                title="Skills"
                items={analysis.skills}
            />

            <ListSection
                title="Strengths"
                items={analysis.strengths}
            />

            <ListSection
                title="Weaknesses"
                items={analysis.weaknesses}
            />

            <EducationSection
                education={analysis.education}
            />

            <ExperienceSection
                experience={analysis.experience}
            />

            <ProjectsSection
                projects={analysis.projects}
            />

        </div>
    );
}

export default ResumeAnalysis;