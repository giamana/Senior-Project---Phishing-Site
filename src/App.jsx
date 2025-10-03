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

import React from "react"
import { BrowserRouter, Routes, Route } from 'react-router-dom';



function App() {

  return (
    <BrowserRouter>
        <NavBar />

        <Routes>
           <Route path="/" element={<HomePage />} />
           <Route path="/about" element={<AboutPage />} />
           <Route path="/login" element={<LoginPage />} />
           <Route path="/platform" element={<PlatformPage />} />
           <Route path="/resources" element={<ResourcesPage />} />
           <Route path="/summary" element={<SummaryPage />} />
           <Route path="/demo" element={<WatchDemoPage />} />
           <Route path="/signUp" element={<SignUpPage />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App
