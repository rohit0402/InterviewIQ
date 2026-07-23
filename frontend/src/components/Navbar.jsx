import { useSelector } from "react-redux";

function Navbar() {
  const user = useSelector((state) => state.auth.user);

  return (
    <header className="h-16 bg-white border-b px-6 flex items-center justify-between shadow-sm">
      <h1 className="text-xl font-bold">
        InterviewIQ
      </h1>

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
          {user?.full_name?.charAt(0).toUpperCase()}
        </div>

        <div>
          <p className="font-semibold">
            {user?.full_name}
          </p>

          <p className="text-sm text-gray-500">
            {user?.email}
          </p>
        </div>
      </div>
    </header>
  );
}

export default Navbar;