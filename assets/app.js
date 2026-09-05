const API_BASE = "https://myhublogistic-api.onrender.com/api";

const TOKEN_KEY = "myhub_token";
const USER_KEY = "myhub_user";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function getUser() {
  const u = localStorage.getItem(USER_KEY);
  return u ? JSON.parse(u) : null;
}

function setUser(user) {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

function logout() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  window.location.href = "login.html";
}

function requireAuth() {
  const user = getUser();
  if (!user) {
    window.location.href = "login.html";
  }
}

function requireAdmin() {
  const user = getUser();
  if (!user || user.role !== "admin") {
    alert("Admin access required");
    window.location.href = "login.html";
  }
}

async function apiRequest(path, options = {}) {
  const url = API_BASE + path;
  const token = getToken();
  const headers = options.headers || {};
  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }
  if (!headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(url, {
    ...options,
    headers,
  });
  if (!res.ok) {
    const err = new Error(res.statusText || "Request failed");
    err.status = res.status;
    try {
      err.data = await res.json();
    } catch {}
    throw err;
  }
  if (res.status === 204) return null;
  return res.json();
}

function el(tag, attrs = {}, children = []) {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === "textContent" || k === "innerHTML" || k === "value" || k === "className" || k === "id" || k === "type" || k === "href" || k === "onclick") {
      e[k] = v;
    } else {
      e.setAttribute(k, v);
    }
  });
  (Array.isArray(children) ? children : [children]).forEach(c => {
    if (typeof c === "string") e.appendChild(document.createTextNode(c));
    else if (c) e.appendChild(c);
  });
  return e;
}

function showMsg(container, message, type) {
  if (!message) {
    container.innerHTML = "";
    return;
  }
  const color = type === "success" ? "green" : "red";
  container.innerHTML = `<p style="color:${color};margin:0 0 10px;">${message}</p>`;
}
