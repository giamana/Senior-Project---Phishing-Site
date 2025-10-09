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

      <header className=" text-black py-8">
        <div className="container mx-auto px-6 text-center">
          <h1 className="text-4xl font-bold">About Phishing Awareness</h1>
          <p className="mt-2 text-lg">Protecting our airline and our passengers from phishing attacks</p>
        </div>
      </header>

      <main className="container mx-auto px-6 py-12">
        <section className="mb-12">
          <h2 className="text-2xl font-semibold mb-4">Why Phishing Matters</h2>
          <p className="text-gray-700 leading-relaxed">
            Phishing is one of the top entry points for cybersecurity breaches. Airline employees are particularly
            vulnerable because attackers can attempt to gain sensitive information, impersonate staff, or access
            critical operational systems. Understanding phishing tactics is key to keeping both employees and
            passengers safe.
          </p>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
          <p className="text-gray-700 leading-relaxed">
            Our goal is to provide comprehensive phishing awareness training to all airline employees. We simulate
            phishing attempts in a controlled environment so staff can recognize malicious messages and respond
            appropriately. By fostering a culture of vigilance, we minimize risks and protect sensitive data.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Key Focus Areas</h2>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li>Recognizing suspicious emails and messages</li>
            <li>Preventing unauthorized access to employee accounts</li>
            <li>Protecting passenger data and company operations</li>
            <li>Responding effectively to phishing attempts</li>
          </ul>
        </section>
      </main>
    </div>
  );
}

export default HomePage;
