// src/views/LoginPage.jsx
import "../App.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "../auth/AuthProvider";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function LoginPage() {
  const navigate = useNavigate();
  const emailRef = useRef();
  const passwordRef = useRef();
  const { login } = useAuth();
  const [error, setError] = useState(null);

  const redirectByRole = (role) => {
    switch (role) {
      case "employee": navigate("/employee"); break;
      case "employer": navigate("/employer"); break;
      case "developer": navigate("/dev"); break;
      default: navigate("/");
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    const email = emailRef.current.value.trim();
    const userPassword = passwordRef.current.value;

    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password: userPassword }),
      });
      const data = await res.json();

      if (res.ok && data.access_token) {
        login(data.access_token, data.role);
        redirectByRole(data.role);
      } else {
        const message = typeof data.detail === "string"
          ? data.detail
          : data.detail?.msg || "Login failed";
        setError(message);
      }
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
        .then((user) => console.log("Google OAuth Name:", user.name))
        .catch((err) => console.error("Google OAuth error:", err));
    }
  }, []);

  const handleGoogleLogin = () => {
    window.location.href =
      "https://accounts.google.com/o/oauth2/v2/auth?client_id=227962041465-upajvn9aq5ec949qa6t7pmkkgoi88qb3.apps.googleusercontent.com&redirect_uri=http://localhost:5173&response_type=token&scope=email profile";
  };

  return (
    <div className="flex">
      <div className="flex w-1/2">
        <img
          src="https://i.pinimg.com/736x/d9/39/e2/d939e20093652518af872c7f7615e56f.jpg"
          alt="Login background"
          className="w-full h-screen object-cover"
        />
      </div>

      <div className="w-1/2 flex flex-col justify-start items-center bg-white mt-20">
        <div className="flex text-6xl font-bold mb-2">
          <h1 className="text-gray-300 mr-2">Welcome</h1>
          <h1 className="text-black">Back</h1>
        </div>

        <div className="w-1/2 text-left mb-4">
          <h3 className="text-gray-400 text-xl">Please log into your account.</h3>
        </div>

        {error && <p className="text-red-600 text-sm mb-4 text-center w-1/2">{error}</p>}

        <form onSubmit={handleSubmit} className="flex flex-col w-full items-center justify-center">
          <input
            id="email"
            type="email"
            placeholder="Email"
            ref={emailRef}
            required
            className="bg-gray-100 mt-2 border border-gray-300 text-lg w-1/2 p-2"
          />
          <input
            id="password"
            type="password"
            placeholder="Password"
            ref={passwordRef}
            required
            className="bg-gray-100 mt-7 border border-gray-300 text-lg w-1/2 p-2"
          />
          <button type="submit" className="bg-black hover:bg-[#CDCDCD] text-white font-bold py-3 px-10 mx-5 mt-6">
            Login
          </button>
        </form>

        <div className="flex mt-6">
          <button
            onClick={() => navigate("/signUp")}
            className="bg-white hover:bg-[#CDCDCD] border border-black text-black font-bold py-3 px-10 mx-7"
          >
            Sign Up
          </button>
        </div>

        <div className="text-neutral-500 flex mt-8 w-1/2 items-center">
          <hr className="flex-grow border-t border-neutral-400" />
          <span className="px-2 text-sm">OR SIGN IN WITH</span>
          <hr className="flex-grow border-t border-neutral-400" />
        </div>

        <button
          onClick={handleGoogleLogin}
          className="flex items-center justify-center gap-3 w-1/2 bg-black text-white py-2 shadow-md mt-4 hover:bg-[#CDCDCD] hover:text-black border border-neutral-800"
        >
          <span className="text-sm font-semibold">Google</span>
        </button>
      </div>
    </div>
  );
}

export default LoginPage;
