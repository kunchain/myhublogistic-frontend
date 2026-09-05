// TODO: Replace with your Render backend URL after deployment
const API_BASE = "https://myhublogistic-api.onrender.com/api";

function getToken(){ return localStorage.getItem("mh_token"); }
function setToken(t){ localStorage.setItem("mh_token", t); }
function clearToken(){ localStorage.removeItem("mh_token"); }
function getUser(){ const u = localStorage.getItem("mh_user"); return u ? JSON.parse(u) : null; }
function setUser(u){ localStorage.setItem("mh_user", JSON.stringify(u)); }
function clearUser(){ localStorage.removeItem("mh_user"); }
function isLoggedIn(){ return !!getToken(); }
function requireAuth(){ if(!isLoggedIn()) window.location.href = "login.html"; }
function requireAdmin(){ requireAuth(); const u = getUser(); if(!u || u.role !== "admin") window.location.href = "client-dashboard.html"; }
function logout(){ clearToken(); clearUser(); window.location.href = "login.html"; }

async function apiRequest(path, options={}){
  const token = getToken();
  const headers = {"Content-Type":"application/json", ...(options.headers||{})};
  if(token) headers["Authorization"] = "Bearer " + token;
  const res = await fetch(API_BASE + path, {...options, headers});
  let data = null;
  const ct = res.headers.get("content-type") || "";
  if(ct.includes("application/json")) data = await res.json();
  if(!res.ok){
    const err = new Error(data?.detail || "Request failed");
    err.status = res.status; err.data = data; throw err;
  }
  return data;
}

function el(tag, attrs={}, children=[]){
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k,v])=>{
    if(k==="className") e.className = v;
    else if(k==="textContent") e.textContent = v;
    else if(k==="innerHTML") e.innerHTML = v;
    else if(k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v);
  });
  (Array.isArray(children) ? children : [children]).forEach(c=>{
    if(typeof c === "string") e.appendChild(document.createTextNode(c));
    else if(c) e.appendChild(c);
  });
  return e;
}

function showMsg(container, text, type="error"){
  const msg = el("div", {
    className: "msg " + (type==="success" ? "msg-success" : "msg-error"),
    textContent: text
  });
  container.innerHTML = "";
  container.appendChild(msg);
}
