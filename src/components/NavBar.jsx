import { NavLink } from "react-router-dom";
import React from "react";
import { useAuth } from "../auth/AuthProvider";
import { useNavigate } from "react-router-dom";

function NavBar({ className, hideButton }) {
  const { logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/signUp"); // redirect after logout
  };

  return (
    <nav className={`${className} bg-black`}>
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-center">
          <div className="flex items-center">
            <div className="hidden sm:flex space-x-4 ml-6">
              {/* Main navigation links */}
              <NavLink
                to="/"
                className={({ isActive }) =>
                  isActive
                    ? "text-yellow-400 px-3 py-2 rounded-md text-m font-bold"
                    : "text-white hover:bg-[#CDCDCD] px-3 py-2 rounded-md text-m"
                }
              >
                Home
              </NavLink>
              <NavLink
                to="/platform"
                className={({ isActive }) =>
                  isActive
                    ? "text-yellow-400 px-3 py-2 rounded-md text-m font-bold"
                    : "text-white hover:bg-[#CDCDCD] px-3 py-2 rounded-md text-m"
                }
              >
                Platform
              </NavLink>
              <NavLink
                to="/resources"
                className={({ isActive }) =>
                  isActive
                    ? "text-yellow-400 px-3 py-2 rounded-md text-m font-bold"
                    : "text-white hover:bg-[#CDCDCD] px-3 py-2 rounded-md text-m"
                }
              >
                Resources
              </NavLink>
              <NavLink
                to="/about"
                className={({ isActive }) =>
                  isActive
                    ? "text-yellow-400 px-3 py-2 rounded-md text-m font-bold"
                    : "text-white hover:bg-[#CDCDCD] px-3 py-2 rounded-md text-m"
                }
              >
                About
              </NavLink>

              {/* Auth buttons */}
              {!hideButton && (
                <>
                  {!isAuthenticated ? (
                    <>
                      <NavLink
                        to="/login"
                        className="bg-[#CDCDCD] text-black font-bold py-2 px-4 rounded"
                      >
                        Login
                      </NavLink>
                      <NavLink
                        to="/signUp"
                        className="bg-[#CDCDCD] text-black font-bold py-2 px-4 rounded"
                      >
                        Sign Up
                      </NavLink>
                    </>
                  ) : (
                    <button
                      onClick={handleLogout}
                      className="bg-red-600 text-white font-bold py-2 px-4 rounded hover:bg-red-800"
                    >
                      Logout
                    </button>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
