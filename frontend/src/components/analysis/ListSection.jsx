function ListSection({ title, items }) {

    if (!items?.length) return null;

    return (
        <div className="rounded-xl bg-white p-6 shadow">

            <h2 className="font-semibold text-xl mb-4">
                {title}
            </h2>

            <ul className="list-disc pl-5 space-y-2">

                {items.map((item, index) => (
                    <li key={index}>
                        {item}
                    </li>
                ))}

            </ul>

        </div>
    );
}

export default ListSection;