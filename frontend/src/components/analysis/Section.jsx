function Section({ title, content }) {
    if (!content) return null;

    return (
        <div className="rounded-xl bg-white p-6 shadow">
            <h2 className="font-semibold text-xl mb-3">
                {title}
            </h2>

            <p className="text-gray-700">
                {content}
            </p>
        </div>
    );
}

export default Section;