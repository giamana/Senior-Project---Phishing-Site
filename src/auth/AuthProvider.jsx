
// src/auth/AuthProvider.jsx
import React, { createContext, useContext, useMemo, useState, useEffect } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(() => {
    // Bootstrap from localStorage on initial render
    try {
      const token = localStorage.getItem("token") || null;
      const role = localStorage.getItem("role") || null;
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      return token ? { token, role, user } : { token: null, role: null, user: null };
    } catch {
      return { token: null, role: null, user: null };
    }
  });

  // Keep context in sync with localStorage changes (optional)
  useEffect(() => {
    const handler = () => {
      try {
        const token = localStorage.getItem("token") || null;
        const role = localStorage.getItem("role") || null;
        const user = JSON.parse(localStorage.getItem("user") || "{}");
        setAuth(token ? { token, role, user } : { token: null, role: null, user: null });
      } catch {}
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, []);

  const login = (token, role, userObj) => {
    localStorage.setItem("token", token);
    if (role) localStorage.setItem("role", (role || "").toLowerCase());
    if (userObj) localStorage.setItem("user", JSON.stringify(userObj));
    setAuth({
      token,
      role: (role || "").toLowerCase(),
      user: userObj || (JSON.parse(localStorage.getItem("user") || "{}") || null),
    });
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("user");
    setAuth({ token: null, role: null, user: null });
  };

  const value = useMemo(() => ({ ...auth, login, logout }), [auth]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
