function EducationSection({ education }) {

    if (!education?.length) return null;

    return (
        <div className="rounded-xl bg-white p-6 shadow">

            <h2 className="font-semibold text-xl mb-4">
                Education
            </h2>

            {education.map((edu, index) => (
                <div
                    key={index}
                    className="border-b py-3 last:border-none"
                >
                    {Object.entries(edu).map(([key, value]) => (
                        <p key={key}>
                            <strong>{key}:</strong> {String(value)}
                        </p>
                    ))}
                </div>
            ))}

        </div>
    );
}

export default EducationSection;