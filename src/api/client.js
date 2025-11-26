const DEFAULT_BASE_URL = "http://localhost:5000";

export const API_BASE_URL =
  (import.meta.env.VITE_API_URL || DEFAULT_BASE_URL).replace(/\/$/, "");

async function parseResponse(response) {
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function handleResponse(response) {
  const data = await parseResponse(response);
  if (!response.ok) {
    const message =
      (data && (data.error || data.message || data.status)) ||
      response.statusText ||
      "Request failed";
    throw new Error(message);
  }
  return data;
}

function normalizePath(path) {
  if (!path.startsWith("/")) {
    return `/${path}`;
  }
  return path;
}

export async function apiGet(path) {
  const url = `${API_BASE_URL}${normalizePath(path)}`;
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
  });
  return handleResponse(response);
}

export async function apiPost(path, body, options = {}) {
  const url = `${API_BASE_URL}${normalizePath(path)}`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    body: body ? JSON.stringify(body) : "{}",
  });
  return handleResponse(response);
}
