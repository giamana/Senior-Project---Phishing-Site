import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import NavBar from './components/NavBar'
import HomePage from "./views/HomePage"
import LoginPage from "./views/LoginPage"
import PlatformPage from "./views/PlatformPage"
import ResourcesPage from "./views/ResourcesPage"
import SummaryPage from "./views/SummaryPage"
import WatchDemoPage from "./views/WatchDemoPage"
import AboutPage from "./views/AboutPage"
import SignUpPage from "./views/SignUpPage"
import EmployeeDetailPage from "./views/EmployeeDetailPage"

import React from "react"
import { BrowserRouter, Routes, Route, useLocation, useNavigate } from 'react-router-dom';


function NavBarWrapper() {
    const location = useLocation();
    let navProps;

    const defaultProps = {
      className:
        "shadow-md bg-[#181818]/75 fixed top-0 z-20 w-3/5 justify-center items-center left-1/2 transform -translate-x-1/2",
    };

    const platformProps = {
      className: "shadow-md bg-[#404143] fixed top-0 z-20 w-full justify-center items-center",
    };

    if (location.pathname === "/login" || location.pathname === "/signUp") {
      return null;
    }

    // Define onPlatform upfront
    const onPlatform =
      location.pathname === "/platform" ||
      location.pathname === "/summary" ||
      location.pathname === "/resources" ||
      location.pathname === "/demo" ||
      location.pathname.startsWith("/platform") ||
      location.pathname.startsWith("/employees");

    if (onPlatform) {
      navProps = platformProps;
    } else {
      navProps = defaultProps;
    }

    const hideButton = onPlatform;

    return <NavBar {...navProps} hideButton={hideButton} />;
  }




function App() {
  return (
    <BrowserRouter>
        <NavBarWrapper />

        <Routes>
           <Route path="/" element={<HomePage />} />
           <Route path="/about" element={<AboutPage />} />
           <Route path="/login" element={<LoginPage />} />
           <Route path="/platform" element={<PlatformPage />} />
           <Route path="/employees/:id" element={<EmployeeDetailPage />} />
           <Route path="/resources" element={<ResourcesPage />} />
           <Route path="/summary" element={<SummaryPage />} />
           <Route path="/demo" element={<WatchDemoPage />} />
           <Route path="/signUp" element={<SignUpPage />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App;
