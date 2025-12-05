// src/views/LoginPage.jsx
import "../App.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "../auth/AuthProvider";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const loginPath = `${API_URL}/api/login`;

const norm = (v) => (typeof v === "string" ? v.toLowerCase() : "");
const roleHome = (role) =>
  norm(role) === "employer" ? "/employer" :
  norm(role) === "developer" ? "/dev" : "/employee";

function LoginPage() {
  const navigate = useNavigate();
  const emailRef = useRef();
  const passwordRef = useRef();
  const { login } = useAuth();
  const [error, setError] = useState(null);

  const redirectByRole = (role) => navigate(roleHome(role));

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    const email = emailRef.current.value.trim();
    const userPassword = passwordRef.current.value;

    try {
      const res = await fetch(loginPath, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password: userPassword }),
      });

      const data = await res.json();

      const token = data.token || data.access_token;
      const role = data.user?.role || data.role;

      if (res.ok && token) {
        localStorage.setItem("token", token);
        if (role) localStorage.setItem("role", norm(role));

        const userObj = {
          id: data.user?.id ?? null,
          first_name: data.user?.first_name ?? "",
          last_name: data.user?.last_name ?? "",
          email: data.user?.email ?? email,
          role: norm(data.user?.role ?? role ?? "employee"),
          companyId: data.user?.companyId ?? null,
          companyName: data.user?.companyName ?? "",
        };

        localStorage.setItem("user", JSON.stringify(userObj));
        login(token, role, userObj);
        redirectByRole(role);

      } else {
        const message =
          typeof data.detail === "string"
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
        .then((user) => {
          const defaultRole = "employee";
          const [firstName, ...lastParts] = (user.name || "User").split(" ");
          const lastName = lastParts.join(" ");

          const userObj = {
            id: null,
            first_name: firstName,
            last_name: lastName,
            email: user.email,
            role: defaultRole,
          };

          localStorage.setItem("token", token);
          localStorage.setItem("role", defaultRole);
          localStorage.setItem("user", JSON.stringify(userObj));

          login(token, defaultRole, userObj);
          redirectByRole(defaultRole);
        })
        .catch((err) => console.error("Google OAuth error:", err));
    }
  }, [login]);


  const handleGoogleLogin = () => {
    window.location.href =
      "https://accounts.google.com/o/oauth2/v2/auth?client_id=227962041465-upajvn9aq5ec949qa6t7pmkkgoi88qb3.apps.googleusercontent.com&redirect_uri=http://localhost:5173&response_type=token&scope=email profile";
  };

  return (
    <div className="flex">
      <div className="flex w-1/2 relative">
        <img
          src="https://i.pinimg.com/736x/d9/39/e2/d939e20093652518af872c7f7615e56f.jpg"
          alt="Login background"
          className="w-full h-screen object-cover"
        />
        <div className="absolute top-10 left-10 flex text-6xl font-bold">
          <h1 className="text-gray-300 mr-2">Welcome</h1>
          <h1 className="text-black">Back</h1>
        </div>
      </div>

      <div className="w-1/2 p-8">
        <h3 className="text-gray-400 text-xl mb-4">Please log into your account.</h3>

        {error && <p className="text-red-600 text-sm mb-4 text-center">{error}</p>}

        <form onSubmit={handleSubmit} className="flex flex-col items-center">
          <input
            id="email"
            type="email"
            placeholder="Email"
            ref={emailRef}
            required
            className="bg-gray-100 mt-2 border border-gray-300 text-lg w-3/4 p-2"
          />
          <input
            id="password"
            type="password"
            placeholder="Password"
            ref={passwordRef}
            required
            className="bg-gray-100 mt-7 border border-gray-300 text-lg w-3/4 p-2"
          />
          <button type="submit" className="bg-black hover:bg-[#CDCDCD] text-white font-bold py-3 px-10 mt-6">
            Login
          </button>
        </form>

        <div className="flex mt-6 justify-center">
          <button
            onClick={() => navigate("/signUp")}
            className="bg-white hover:bg-[#CDCDCD] border border-black text-black font-bold py-3 px-10"
          >
            Sign Up
          </button>
        </div>

        <div className="text-neutral-500 flex mt-8 items-center">
          <hr className="flex-grow border-t border-neutral-400" />
          <span className="px-2 text-sm">OR SIGN IN WITH</span>
          <hr className="flex-grow border-t border-neutral-400" />
        </div>

        <button
          onClick={handleGoogleLogin}
          className="flex items-center justify-center gap-3 w-full bg-black text-white py-2 shadow-md mt-4 hover:bg-[#CDCDCD] hover:text-black border border-neutral-800"
        >
          <span className="text-sm font-semibold">Google</span>
        </button>
      </div>
    </div>
  );
}

export default LoginPage;
