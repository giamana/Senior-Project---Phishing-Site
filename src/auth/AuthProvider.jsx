import React, { createContext, useContext, useMemo, useState, useEffect } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(() => {
    try {
      const token = localStorage.getItem("token") || null;
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      return token ? { token, user } : { token: null, user: null };
    } catch {
      return { token: null, user: null };
    }
  });

  useEffect(() => {
    const handler = () => {
      try {
        const token = localStorage.getItem("token") || null;
        const user = JSON.parse(localStorage.getItem("user") || "{}");
        setAuth(token ? { token, user } : { token: null, user: null });
      } catch {}
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, []);

  // ---- API calls ----
  const signup = async (name, email, password, phone, employerId) => {
    const payload = { name, email, password, phone, employerId, role: "employer" };
    console.log("Signup payload:", payload);

    const res = await fetch("http://localhost:5000/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) {
      console.error("Signup failed:", data);
      throw new Error(data.error || "Signup failed");
    }

    localStorage.setItem("employerId", data.employerId);
    login(data.access_token, {
      id: data.id,
      name: data.name,
      email: data.email,
      phone: data.phone,
      employerId: data.employerId,
      role: data.role,
    });
    return data;
  };

  const signin = async (email, password) => {
    const payload = { email, password };
    console.log("Signin payload:", payload);

    const res = await fetch("http://localhost:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) {
      console.error("Login failed:", data);
      throw new Error(data.error || "Login failed");
    }

    localStorage.setItem("employerId", data.employerId);
    login(data.access_token, {
      id: data.id,
      name: data.name,
      email: data.email,
      phone: data.phone,
      employerId: data.employerId,
      role: data.role,
    });
    return data;
  };

  const logout = async () => {
    const token = localStorage.getItem("token");
    if (token) {
      await fetch("http://localhost:5000/api/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token }),
      });
    }
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setAuth({ token: null, user: null });
  };

  const login = (token, userObj) => {
    localStorage.setItem("token", token);
    if (userObj) localStorage.setItem("user", JSON.stringify(userObj));
    setAuth({ token, user: userObj || null });
  };

  const value = useMemo(
    () => ({
      authUser: auth.user,
      token: auth.token,
      login,
      logout,
      signup,
      signin,
    }),
    [auth]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
