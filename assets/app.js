// Myhublogistic frontend app helpers
// Configure API_BASE_URL below or in config.js

const API_BASE_URL = "http://localhost:8000"; // Change to your backend URL

// --- Auth helpers ---

function setToken(token) {
  localStorage.setItem("ml_token", token);
}

function getToken() {
  return localStorage.getItem("ml_token");
}

function clearToken() {
  localStorage.removeItem("ml_token");
}

// Decode JWT to get payload (including user id in "sub")
function decodeJwt(token) {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map(c => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

function getUser() {
  const token = getToken();
  if (!token) return null;
  const payload = decodeJwt(token);
  if (!payload || !payload.sub) return null;
  return { id: payload.sub };
}

function setUser(userData) {
  // No-op with JWT; user info comes from token payload
}

function logout() {
  clearToken();
  window.location.href = "index.html";
}

function requireAdmin() {
  const user = getUser();
  if (!user) {
    window.location.href = "login.html";
    return;
  }
}

function requireClient() {
  const user = getUser();
  if (!user) {
    window.location.href = "login.html";
    return;
  }
}

// --- API helpers ---

async function apiRequest(path, options = {}) {
  const token = getToken();
  const url = API_BASE_URL + (path.startsWith("/") ? path : "/" + path);

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers["Authorization"] = token;
  }

  const res = await fetch(url, {
    ...options,
    headers,
  });

  if (!res.ok) {
    let errData = {};
    try {
      errData = await res.json();
    } catch (e) {}
    const err = new Error(errData.detail || `HTTP ${res.status}`);
    err.status = res.status;
    err.data = errData;
    throw err;
  }

  if (res.status === 204) return null;
  return await res.json();
}

// --- UI helpers ---

function el(tag, attrs = {}, children = []) {
  const element = document.createElement(tag);
  Object.entries(attrs).forEach(([key, value]) => {
    if (key === "className") element.className = value;
    else if (key === "onclick") element.onclick = value;
    else if (key.startsWith("on")) element.addEventListener(key.slice(2).toLowerCase(), value);
    else element.setAttribute(key, value);
  });
  if (!Array.isArray(children)) children = [children];
  children.forEach(c => {
    if (typeof c === "string") element.appendChild(document.createTextNode(c));
    else if (c) element.appendChild(c);
  });
  return element;
}

function showMsg(container, text, type = "error") {
  if (!text) {
    container.innerHTML = "";
    return;
  }
  const color = type === "success" ? "var(--success)" : "var(--danger)";
  container.innerHTML = `<div style="padding:10px;border-radius:6px;background:rgba(255,255,255,0.06);border:1px solid ${color};color:${color};margin-bottom:12px;font-size:14px;">${text}</div>`;
}
