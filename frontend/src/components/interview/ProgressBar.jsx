function ProgressBar({ sequence }) {
    const progress = Math.min(sequence * 10, 100);

    return (
        <div className="bg-white rounded-xl shadow-sm border p-5">
            <div className="flex justify-between mb-2">
                <h3 className="font-semibold">
                    Technical Interview
                </h3>

                <span className="text-sm text-gray-500">
                    Question {sequence}
                </span>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                    className="bg-indigo-600 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${progress}%` }}
                />
            </div>
        </div>
    );
}

export default ProgressBar;