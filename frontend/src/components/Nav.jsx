import { Link, useNavigate } from "react-router-dom";
import { logout } from "../utils/auth";
import { useState } from "react";

export default function Nav() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Left */}
        <div className="flex items-center gap-6">
          <span
            className="text-lg font-semibold cursor-pointer"
            onClick={() => navigate("/po-dashboard")}
          >
            Procument APP
          </span>

          <Link to="/po-dashboard" className="text-sm text-gray-600 hover:text-black">
            Dashboard
          </Link>
          <Link to="/vendors" className="text-sm text-gray-600 hover:text-black">
            Vendors
          </Link>
          <Link to="/create-po" className="text-sm text-gray-600 hover:text-black">
            Create PO
          </Link>
          <Link to="/agent" className="text-sm text-gray-600 hover:text-black">
            AI Agent
          </Link>
        </div>

        {/* Right */}
        <div className="relative">
          <button
            onClick={() => setOpen(!open)}
            className="flex items-center gap-2 text-sm font-medium"
          >
            Account
            <span className="text-gray-400">▾</span>
          </button>

          {open && (
            <div className="absolute right-0 mt-2 w-40 bg-white border rounded-lg shadow-lg">
              <button
                onClick={logout}
                className="w-full text-left px-4 py-2 text-sm hover:bg-gray-100"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
