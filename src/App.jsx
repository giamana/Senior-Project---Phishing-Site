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
import { AuthProvider, useAuth } from "./context/AuthContext"

import React from "react"
import { BrowserRouter, Routes, Route, useLocation, useNavigate, Navigate } from 'react-router-dom';
import VirusPage from './views/VirusPage'


function NavBarWrapper() {
    const location = useLocation();
    const { authUser } = useAuth();
    let navProps;

    // left-1/2 transform -translate-x-1/2
    const defaultProps = {
      className:
        "shadow-md bg-[#181818]/25 fixed top-0 z-20 w-full justify-center items-center ",
    };

    const platformProps = {
      className: "shadow-md bg-[#404143] fixed top-0 z-20 w-full justify-center items-center",
    };

    const homeProps = {
      className: "shadow-md bg-[#181818]/75 fixed top-0 z-20 w-full justify-center items-center",
    };

    const onPlatform =
      location.pathname === "/platform" ||
      location.pathname === "/info" ||
      location.pathname === "/highest" ||
      location.pathname === "/lowest" ||
      location.pathname === "/highest-risk" ||
      location.pathname === "/lowest-risk" ||
      location.pathname === "/demo" ||
      location.pathname.startsWith("/platform") ||
      location.pathname.startsWith("/employees");

    if (location.pathname === "/login" || location.pathname === "/signUp" || location.pathname === "/virus") {
      return null;
    }

  if (onPlatform) {
      navProps = platformProps;
    } 
    else {
      navProps = defaultProps;
    }

    const hideButton = onPlatform;

    return <NavBar {...navProps} hideButton={hideButton} isAuthenticated={!!authUser} />;
  }


function ProtectedRoute({ children }) {
  const { authUser } = useAuth();
  if (!authUser || authUser.role !== "employer") {
    return <Navigate to="/login" replace />;
  }
  return children;
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
             <Route path="/platform" element={<ProtectedRoute><PlatformPage /></ProtectedRoute>} />
             <Route path="/employees/:id" element={<EmployeeDetailPage />} />
             <Route path="/resources" element={<ResourcesPage />} />
             <Route path="/demo" element={<WatchDemoPage />} />
             <Route path="/signUp" element={<SignUpPage />} />
             <Route path="/highest" element={<ProtectedRoute><HighestRisks /></ProtectedRoute>} />
             <Route path="/highest-risk" element={<ProtectedRoute><HighestRisks /></ProtectedRoute>} />
             <Route path="/lowest" element={<ProtectedRoute><LowestRisks/></ProtectedRoute>} />
             <Route path="/lowest-risk" element={<ProtectedRoute><LowestRisks/></ProtectedRoute>} />
             <Route path="/virus" element={<VirusPage/>} />
          </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
