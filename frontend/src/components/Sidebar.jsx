import { NavLink } from "react-router-dom";
import { logoutUser } from "../utils/auth";

function Sidebar() {
  const linkStyle = ({ isActive }) =>
    `block px-4 py-3 rounded-lg ${
      isActive
        ? "bg-blue-600 text-white"
        : "hover:bg-gray-200"
    }`;

  return (
    <aside className="w-64 bg-white border-r p-4 flex flex-col">
      <nav className="space-y-2 flex-1">
        <NavLink to="/dashboard" className={linkStyle}>
          Dashboard
        </NavLink>

        <NavLink to="/resume" className={linkStyle}>
          Resume
        </NavLink>

        <NavLink to="/interviews" className={linkStyle}>
          Interviews
        </NavLink>

        <NavLink to="/reports" className={linkStyle}>
          Reports
        </NavLink>

        <NavLink to="/profile" className={linkStyle}>
          Profile
        </NavLink>
      </nav>

      <button
        onClick={logoutUser}
        className="mt-4 rounded-lg bg-red-500 px-4 py-2 text-white hover:bg-red-600"
      >
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;