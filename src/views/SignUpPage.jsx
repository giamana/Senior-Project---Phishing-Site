// src/views/SignUpPage.jsx
import React, { useRef, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthProvider";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function SignUpPage() {
  const fname = useRef();
  const lname = useRef();
  const email = useRef();
  const password = useRef();
  const company = useRef();
  const navigate = useNavigate();
  const { login } = useAuth();
  const [role, setRole] = useState("employee");
  const [error, setError] = useState(null);

  const redirectByRole = (userRole) => {
    switch (userRole) {
      case "employee": navigate("/employee"); break;
      case "employer": navigate("/employer"); break;
      case "developer": navigate("/dev"); break;
      default: navigate("/");
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    const name = `${fname.current.value} ${lname.current.value}`.trim();
    const userEmail = email.current.value.trim();
    const userPassword = password.current.value;
    const companyName = company.current.value?.trim() || null;

    try {
      const res = await fetch(`${API_URL}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: userEmail,       // using email for identity
          password: userPassword, // ensure backend expects this
          name,
          role,
          company_name: companyName,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        const message = typeof data.detail === "string"
          ? data.detail
          : data.detail?.msg || "Signup failed";
        setError(message);
        return;
      }

      const loginRes = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: userEmail, password: userPassword }),
      });
      const loginData = await loginRes.json();

      if (!loginRes.ok || !loginData.access_token) {
        const message = typeof loginData.detail === "string"
          ? loginData.detail
          : loginData.detail?.msg || "Login failed after signup";
        setError(message);
        return;
      }

      login(loginData.access_token, loginData.role);
      redirectByRole(loginData.role);
    } catch (err) {
      setError("Something went wrong");
    }
  };

  useEffect(() => {
    const hash = window.location.hash;
    if (hash.includes("access_token")) {
      const token = hash.split("access_token=")[1].split("&")[0];
      fetch("https://www.googleapis.com/oauth2/v2/userinfo", {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => res.json())
        .then((user) => {
          const defaultRole = "employee";
          login(token, defaultRole);
          redirectByRole(defaultRole);
        })
        .catch((err) => console.error("Google OAuth error:", err));
    }
  }, []);

  return (
    <div className="relative min-h-screen">
      <img
        src="https://i.pinimg.com/736x/52/d8/d1/52d8d1745e37b41307692ddeea8f8a0e.jpg"
        alt="Background"
        className="absolute inset-0 w-full h-full object-cover"
      />
      <div className="absolute inset-0 bg-black/50"></div>
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="max-w-md w-full bg-black/80 backdrop-blur-md rounded-2xl shadow-2xl p-8">
          <h2 className="text-2xl font-bold text-center text-white mb-6">
            Create an Account
          </h2>

          <div className="flex justify-center mb-6">
            <button
              type="button"
              onClick={() => setRole("employee")}
              className={`px-4 py-2 rounded-l-md ${
                role === "employee" ? "bg-white text-black font-bold" : "bg-gray-700 text-white"
              }`}
            >
              Employee
            </button>
            <button
              type="button"
              onClick={() => setRole("employer")}
              className={`px-4 py-2 ${
                role === "employer" ? "bg-white text-black font-bold" : "bg-gray-700 text-white"
              }`}
            >
              Employer
            </button>
            <button
              type="button"
              onClick={() => setRole("developer")}
              className={`px-4 py-2 rounded-r-md ${
                role === "developer" ? "bg-white text-black font-bold" : "bg-gray-700 text-white"
              }`}
            >
              Developer
            </button>
          </div>

          {error && <p className="text-red-500 mb-4">{error}</p>}

          <form onSubmit={handleSubmit}>
            <div className="flex flex-row gap-3 mb-4">
              <input
                type="text"
                placeholder="First Name"
                ref={fname}
                className="w-1/2 p-2 rounded-md bg-transparent border border-neutral-700 text-white placeholder-neutral-500 shadow-xl"
              />
              <input
                type="text"
                placeholder="Last Name"
                ref={lname}
                className="w-1/2 p-2 rounded-md bg-transparent border border-neutral-700 text-white placeholder-neutral-500"
              />
            </div>

            <input
              type="email"
              placeholder="Email"
              ref={email}
              className="w-full p-2 rounded-md bg-transparent border border-neutral-700 text-white placeholder-neutral-500 mb-4"
            />

            <input
              type="password"
              placeholder="Password"
              ref={password}
              className="w-full p-2 rounded-md bg-transparent border border-neutral-700 text-white placeholder-neutral-500 mb-4"
            />

            {(role === "employee" || role === "employer") && (
              <input
                type="text"
                placeholder="Company Name"
                ref={company}
                className="w-full p-2 rounded-md bg-transparent border border-neutral-700 text-white placeholder-neutral-500 mb-6"
              />
            )}

            <button
              type="submit"
              className="w-full bg-white hover:bg-neutral-800 hover:text-white text-black font-semibold py-2 rounded-md shadow-md transition-all duration-200"
            >
              Create Account
            </button>
          </form>

          <div className="text-neutral-500 flex mt-4 w-full items-center">
            <hr className="flex-grow border-t border-neutral-700" />
            <span className="px-2 text-sm"> OR SIGN IN WITH </span>
            <hr className="flex-grow border-t border-neutral-700" />
          </div>

          <button
            onClick={() => {
              window.location.href =
                "https://accounts.google.com/o/oauth2/v2/auth?client_id=227962041465-upajvn9aq5ec949qa6t7pmkkgoi88qb3.apps.googleusercontent.com&redirect_uri=http://localhost:5173&response_type=token&scope=email profile";
            }}
            className="w-full flex bg-neutral-800 text-black py-2 rounded-md shadow-md mt-4 items-center justify-center hover:bg-white"
          >
            <span className="text-white">Google</span>
          </button>

          <p className="text-center text-neutral-500 text-sm mt-4">
            Already have an account?{" "}
            <a href="/login" className="text-neutral-300 hover:text-neutral-100 underline">
              Sign in
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default SignUpPage;
