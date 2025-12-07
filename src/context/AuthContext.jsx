import React, { createContext, useContext, useEffect, useState } from "react";

const AUTH_KEY = "saas_auth";
const EMPLOYER_ID_KEY = "saas_employer_id";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [authUser, setAuthUser] = useState(() => {
    const saved = localStorage.getItem(AUTH_KEY);
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (authUser) {
      localStorage.setItem(AUTH_KEY, JSON.stringify(authUser));
      if (authUser.role === "employer" && authUser.employerId) {
        localStorage.setItem(EMPLOYER_ID_KEY, String(authUser.employerId));
        localStorage.setItem("employerId", String(authUser.employerId));
      }
    } else {
      localStorage.removeItem(AUTH_KEY);
      localStorage.removeItem(EMPLOYER_ID_KEY);
      localStorage.removeItem("employerId");
      // Clear any auth fragments (e.g., Google tokens) to avoid stale logins blocking fetches.
      if (window.location.hash) {
        window.history.replaceState(null, "", window.location.pathname + window.location.search);
      }
    }
  }, [authUser]);

  const login = (user) => setAuthUser(user);
  const logout = () => setAuthUser(null);

  return (
    <AuthContext.Provider value={{ authUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
