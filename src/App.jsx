import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import NavBar from './components/NavBar'
import HomePage from "./views/HomePage"
import LoginPage from "./views/LoginPage"
import PlatformPage from "./views/PlatformPage"
import ResourcesPage from "./views/ResourcesPage"
import WatchDemoPage from "./views/WatchDemoPage"
import AboutPage from "./views/AboutPage"
import SignUpPage from "./views/SignUpPage"
import EmployeeDetailPage from "./views/EmployeeDetailPage"
import HighestRisks from "./views/HighestRisks"
import LowestRisks from "./views/LowestRisks"
import Info from "./views/Info"

import React from "react"
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import VirusPage from './views/VirusPage'

// ✅ import AuthProvider
import { AuthProvider } from "./auth/AuthProvider";

function NavBarWrapper() {
  const location = useLocation();
  let navProps;

  const defaultProps = {
    className:
      "shadow-md bg-[#181818]/25 fixed top-0 z-20 w-full justify-center items-center ",
  };

  const platformProps = {
    className: "shadow-md bg-[#404143] fixed top-0 z-20 w-full justify-center items-center",
  };

  const onPlatform =
    location.pathname === "/platform" ||
    location.pathname === "/info" ||
    location.pathname === "/resources" ||
    location.pathname === "/highest" ||
    location.pathname === "/lowest" ||
    location.pathname === "/demo" ||
    location.pathname.startsWith("/platform") ||
    location.pathname.startsWith("/employees");

  if (location.pathname === "/login" || location.pathname === "/signUp" || location.pathname === "/virus") {
    return null;
  }

  navProps = onPlatform ? platformProps : defaultProps;
  const hideButton = onPlatform;

  return <NavBar {...navProps} hideButton={hideButton} />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <NavBarWrapper />

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/platform" element={<PlatformPage />} />
          <Route path="/employees/:id" element={<EmployeeDetailPage />} />
          <Route path="/resources" element={<ResourcesPage />} />
          <Route path="/demo" element={<WatchDemoPage />} />
          <Route path="/signUp" element={<SignUpPage />} />
          <Route path="/highest" element={<HighestRisks />} />
          <Route path="/lowest" element={<LowestRisks />} />
          <Route path="/info" element={<Info />} />
          <Route path="/virus" element={<VirusPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
