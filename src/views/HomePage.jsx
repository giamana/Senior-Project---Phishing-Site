import '../App.css';
import NavBar from '../components/NavBar';
import React from 'react';

function HomePage() {
  return (
    <div>
      <div className="pt-16 relative" id="mainPic">
        <img src="bg.png" alt="Background" className="w-full h-screen object-cover" />
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <h1 className="text-white text-8xl font-bold z-10 text-center">Your Crew’s Shield <br />Against Phishing</h1>
          <button class="bg-white hover:bg-[#CDCDCD] text-black font-bold py-5 px-5 rounded mt-5 p-2">Watch Our Demo</button>
        </div>
      </div> 
    </div>
  );
}

export default HomePage;
