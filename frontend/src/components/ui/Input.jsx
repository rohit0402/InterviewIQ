
const Input = ({label,type = "text",name,register,rules = {},error,placeholder,}) => {
  return (
    <div className="mb-5">
      {label && (
        <label className="mb-2 block text-sm font-medium text-gray-700">
          {label}
        </label>
      )}

      <input
        type={type}
        placeholder={placeholder}
        {...register(name, rules)}
        className={`w-full rounded-lg border px-4 py-3 outline-none transition
          ${
            error
              ? "border-red-500 focus:ring-2 focus:ring-red-400"
              : "border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-400"
          }`}
      />

      {error && (
        <p className="mt-1 text-sm text-red-500">{error.message}</p>
      )}
    </div>
  );
};

export default Input;