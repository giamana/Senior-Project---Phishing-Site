import "../App.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useRef } from "react";
import { useAuth } from "../auth/AuthProvider"; // <-- import your provider

function LoginPage() {
  const navi = useNavigate();
  const emailRef = useRef();
  const passwordRef = useRef();
  const auth = useAuth();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const email = emailRef.current.value;
      const password = passwordRef.current.value;
      const data = await auth.signin(email, password);
      console.log("Logged in:", data);
      navi("/platform"); // redirect after login
    } catch (err) {
      alert(err.message);
    }
  };

  useEffect(() => {
    if (authUser && authUser.role === "employer") {
      navigate('/platform', { replace: true });
      return;
    }
    const hash = window.location.hash;
    if (hash.includes("access_token")) {
      const token = hash.split("access_token=")[1].split("&")[0];
      fetch("https://www.googleapis.com/oauth2/v2/userinfo", {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => res.json())
        .then((user) => {
          console.log("Google user:", user);
          // You could call auth.login(token, user) here if you want to integrate Google login
        });
    }
  }, [auth]);

  return (
    <div className="flex">
      <div className="flex w-1/2">
        <img
          src="https://i.pinimg.com/736x/d9/39/e2/d939e20093652518af872c7f7615e56f.jpg"
          alt=""
          className="w-full h-screen"
        />
      </div>

      <div className="w-1/2 flex flex-col justify-start items-center bg-white mt-25">
        <div className="flex text-6xl font-bold mb-2 mt-20">
          <h1 className="text-gray-300 mr-2">Welcome</h1>
          <h1 className="text-black">Back</h1>
        </div>

        <div className="w-1/2 text-left mb-4">
          <h3 className="text-gray-400 text-xl">Please log into your account.</h3>
        </div>

        <form
          onSubmit={handleSubmit}
          className="flex flex-col w-full items-center justify-center"
        >
          <input
            type="email"
            placeholder="Email"
            ref={emailRef}
            className="bg-gray-100 mt-2 border border-gray-300 text-lg w-1/2 p-2"
          />
          <input
            type="password"
            placeholder="Password"
            ref={passwordRef}
            className="bg-gray-100 mt-7 border border-gray-300 text-lg w-1/2 p-2"
          />
          <button
            type="submit"
            className="bg-black hover:bg-[#CDCDCD] text-white font-bold py-3 px-10 mx-5 mt-6"
          >
            Login
          </button>
        </form>

        <button
          onClick={() => navi("/signUp")}
          className="bg-white hover:bg-[#CDCDCD] border border-black text-black font-bold py-3 px-10 mx-7 mt-4"
        >
          Sign Up
        </button>

        <div className="text-neutral-500 flex mt-8 w-1/2 items-center">
          <hr className="flex-grow border-t border-neutral-400" />
          <span className="px-2 text-sm">OR SIGN IN WITH</span>
          <hr className="flex-grow border-t border-neutral-400" />
        </div>

        <button
          onClick={() => {
            window.location.href =
              "https://accounts.google.com/o/oauth2/v2/auth?client_id=227962041465-upajvn9aq5ec949qa6t7pmkkgoi88qb3.apps.googleusercontent.com&redirect_uri=http://localhost:5173&response_type=token&scope=email profile";
          }}
          className="flex items-center justify-center gap-3 w-1/2 bg-black text-white py-2 shadow-md mt-4 hover:bg-[#CDCDCD] hover:text-black border border-neutral-800 "
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" viewBox="0 0 48 48">
            {/* Google logo paths */}
            <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303..." />
            <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819..." />
            <path fill="#4CAF50" d="M24,44c5.166,0,9.86..." />
            <path fill="#1976D2" d="M43.611,20.083H42V20H24v8..." />
          </svg>
          <span className="text-sm font-semibold">Google</span>
        </button>

        <div className="w-1/2 text-left mt-6 text-sm text-gray-500">
          <p>Signing up means you agree to our Terms & Conditions & Privacy Policy</p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
