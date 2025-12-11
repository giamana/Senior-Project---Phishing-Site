import { Link, useNavigate } from 'react-router-dom';
import React from 'react';
import { useAuth } from '../auth/AuthProvider';


function NavBar({ className, hideButton }) {
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login'); // redirect after logout
  };

  return (
    <nav className={className}>
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-center">
          <div className="flex items-center">
            <div className="hidden sm:flex space-x-4 ml-6">
              <Link to="/" className="text-white hover:bg-[#CDCDCD] hover:text-white px-3 py-2 rounded-md text-m">
                Home
              </Link>
              <Link to="/platform" className="text-white hover:bg-[#CDCDCD] hover:text-white px-3 py-2 rounded-md text-m">
                Platform
              </Link>
              <Link to="/resources" className="text-white hover:bg-[#CDCDCD] hover:text-white px-3 py-2 rounded-md text-m">
                Resources
              </Link>
              <Link to="/about" className="text-white hover:bg-[#CDCDCD] hover:text-white px-3 py-2 rounded-md text-m">
                About
              </Link>

              {!hideButton && (
                token ? (
                  <button
                    onClick={handleLogout}
                    className="bg-[#CDCDCD] hover:bg-gray-300 text-black font-bold px-3 py-2 rounded-md text-m"
                  >
                    Logout
                  </button>
                ) : (
                  <Link
                    to="/login"
                    className="bg-[#CDCDCD] hover:bg-gray-300 text-black font-bold px-3 py-2 rounded-md text-m"
                  >
                    Login
                  </Link>
                )
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
