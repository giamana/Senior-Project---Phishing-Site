import '../App.css';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const navi = useNavigate();

  return (
    <div className="flex">
      <div className="flex w-1/2">
        <img src="login_bg.png" alt="" className="w-full" />
      </div>

      <div className="w-1/2 flex flex-col justify-start mt-45 items-center bg-white">
        <div className="flex text-6xl font-bold mb-2">
          <h1 className="text-gray-300 mr-2">Welcome</h1>
          <h1 className="text-black">Back</h1>
        </div>

        <div className="w-1/2 text-left mb-4">
          <h3 className="text-gray-400 text-xl">Please log into your account.</h3>
        </div>

        <input type="text" className="bg-gray-100 mt-2 border border-gray-300 rounded-xl text-lg w-1/2 p-3" placeholder="Username"
        />
        <input type="password" className="bg-gray-100 mt-7 border border-gray-300 rounded-xl text-lg w-1/2 p-3"placeholder="Password"
        />

        <div className="w-1/2 text-right mt-2">
          <a href="#" className="text-gray-400 hover:text-black text-sm">
            Forgot Password?
          </a>
        </div>


        <div className="flex mt-6">
          <button onClick ={ () => {navi("/platform")}} className="bg-black hover:bg-[#CDCDCD] text-white font-bold py-3 px-10 mx-5">
            Login
          </button>
          <button className="bg-white hover:bg-[#CDCDCD] border border-black text-black font-bold py-3 px-10 mx-7">
            Sign Up
          </button>
        </div>

        <div className="w-1/2 text-left mt-3">
          <p className="text-gray-300">
            Signing up means you agree with giving information to our website
          </p>
          <p className="text-black">Terms & Conditions & Privacy Policy</p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
