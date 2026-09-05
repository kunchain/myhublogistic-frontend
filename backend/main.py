"""
Minimal FastAPI backend stub for Myhublogistic frontend.
In-memory data only; for development/demo purposes.
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timezone
import uuid

app = FastAPI(title="Myhublogistic API")

# --- In-memory "database" ---
USERS = [
    {
        "id": "u_admin",
        "email": "admin@myhublogistic.com",
        "password": "Admin@1234",
        "name": "Admin User",
        "company_name": "Myhublogistic",
        "phone": "",
        "role": "admin",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
]

COMPANIES = []
SHIPMENTS = []
INVOICES = []
PAYMENTS = []

# --- Pydantic models ---

# Auth
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Users
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    company_name: Optional[str] = ""
    phone: Optional[str] = ""
    role: str = "client"

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None

# Shipments
class ShipmentCreateAdmin(BaseModel):
    customer_email: EmailStr
    origin: str
    destination: str
    status: Optional[str] = "pending"
    weight_kg: Optional[float] = None
    tracking_number: Optional[str] = ""

class ShipmentUpdateAdmin(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    status: Optional[str] = None
    weight_kg: Optional[float] = None
    tracking_number: Optional[str] = None

class ShipmentCreateClient(BaseModel):
    origin: str
    destination: str
    weight_kg: Optional[float] = None
    description: Optional[str] = ""

# Invoices
class InvoiceCreateAdmin(BaseModel):
    customer_email: EmailStr
    amount_cents: int
    status: Optional[str] = "pending"
    due_date: Optional[str] = None
    description: Optional[str] = ""

class InvoiceUpdateAdmin(BaseModel):
    customer_email: Optional[EmailStr] = None
    amount_cents: Optional[int] = None
    status: Optional[str] = None
    due_date: Optional[str] = None
    description: Optional[str] = None

# Client profile
class ClientProfileUpdate(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None

# --- Auth helpers ---

def get_current_user(x_authorization: Optional[str] = Header(None)):
    if not x_authorization:
        raise HTTPException(status_code=401, detail="Missing authorization")
    # Simple token == user_id mapping for demo
    user = next((u for u in USERS if u["id"] == x_authorization), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user

def require_client(user: dict = Depends(get_current_user)):
    if user["role"] not in ("client", "admin"):
        raise HTTPException(status_code=403, detail="Client only")
    return user

# --- Endpoints ---

@app.post("/auth/login")
def login(req: LoginRequest):
    user = next((u for u in USERS if u["email"] == req.email and u["password"] == req.password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Return user id as "token" for demo
    return {"access_token": user["id"], "user": {k: v for k, v in user.items() if k != "password"}}

# Admin users
@app.get("/admin/users")
def list_users(admin: dict = Depends(require_admin)):
    return [{k: v for k, v in u.items() if k != "password"} for u in USERS]

@app.post("/admin/users")
def create_user(req: UserCreate, admin: dict = Depends(require_admin)):
    if any(u["email"] == req.email for u in USERS):
        raise HTTPException(status_code=400, detail="Email already exists")
    user = {
        "id": "u_" + uuid.uuid4().hex[:8],
        "email": req.email,
        "password": req.password,
        "name": req.name,
        "company_name": req.company_name or "",
        "phone": req.phone or "",
        "role": req.role or "client",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    USERS.append(user)
    return {k: v for k, v in user.items() if k != "password"}

@app.put("/admin/users/{user_id}")
def update_user(user_id: str, req: UserUpdate, admin: dict = Depends(require_admin)):
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, val in req.dict(exclude_unset=True).items():
        if val is not None:
            user[field] = val
    return {k: v for k, v in user.items() if k != "password"}

@app.delete("/admin/users/{user_id}")
def delete_user(user_id: str, admin: dict = Depends(require_admin)):
    global USERS
    before = len(USERS)
    USERS = [u for u in USERS if u["id"] != user_id]
    if len(USERS) == before:
        raise HTTPException(status_code=404, detail="User not found")
    return {"deleted": user_id}

# Admin shipments
@app.get("/admin/shipments")
def list_shipments_admin(admin: dict = Depends(require_admin)):
    return {"shipments": SHIPMENTS}

@app.post("/admin/shipments")
def create_shipment_admin(req: ShipmentCreateAdmin, admin: dict = Depends(require_admin)):
    shipment = {
        "id": "s_" + uuid.uuid4().hex[:8],
        "customer_email": req.customer_email,
        "origin": req.origin,
        "destination": req.destination,
        "status": req.status or "pending",
        "weight_kg": req.weight_kg,
        "tracking_number": req.tracking_number or "",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    SHIPMENTS.append(shipment)
    return shipment

@app.put("/admin/shipments/{sid}")
def update_shipment_admin(sid: str, req: ShipmentUpdateAdmin, admin: dict = Depends(require_admin)):
    shipment = next((s for s in SHIPMENTS if s["id"] == sid), None)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    for field, val in req.dict(exclude_unset=True).items():
        if val is not None:
            shipment[field] = val
    return shipment

# Admin invoices
@app.get("/admin/invoices")
def list_invoices_admin(admin: dict = Depends(require_admin)):
    return {"invoices": INVOICES}

@app.post("/admin/invoices")
def create_invoice_admin(req: InvoiceCreateAdmin, admin: dict = Depends(require_admin)):
    invoice = {
        "id": "i_" + uuid.uuid4().hex[:8],
        "customer_email": req.customer_email,
        "amount_cents": req.amount_cents,
        "status": req.status or "pending",
        "due_date": req.due_date,
        "description": req.description or "",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    INVOICES.append(invoice)
    return invoice

@app.put("/admin/invoices/{iid}")
def update_invoice_admin(iid: str, req: InvoiceUpdateAdmin, admin: dict = Depends(require_admin)):
    invoice = next((i for i in INVOICES if i["id"] == iid), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    for field, val in req.dict(exclude_unset=True).items():
        if val is not None:
            invoice[field] = val
    return invoice

# Admin DB view
@app.get("/admin/db/{table_name}")
def db_view(table_name: str, admin: dict = Depends(require_admin)):
    data = {
        "users": [{k: v for k, v in u.items() if k != "password"} for u in USERS],
        "companies": COMPANIES,
        "shipments": SHIPMENTS,
        "invoices": INVOICES,
        "payments": PAYMENTS,
    }
    if table_name not in data:
        raise HTTPException(status_code=404, detail="Table not found")
    rows = data[table_name]
    if not rows:
        return {"columns": [], "rows": []}
    columns = list(rows[0].keys())
    return {"columns": columns, "rows": rows}

# Client shipments
@app.get("/client/shipments")
def list_shipments_client(user: dict = Depends(require_client)):
    # For demo: return all shipments; filter by customer_email if desired
    return {"shipments": SHIPMENTS}

@app.post("/client/shipments")
def create_shipment_client(req: ShipmentCreateClient, user: dict = Depends(require_client)):
    shipment = {
        "id": "s_" + uuid.uuid4().hex[:8],
        "customer_email": user["email"],
        "origin": req.origin,
        "destination": req.destination,
        "status": "pending",
        "weight_kg": req.weight_kg,
        "description": req.description or "",
        "tracking_number": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    SHIPMENTS.append(shipment)
    return shipment

# Client invoices
@app.get("/client/invoices")
def list_invoices_client(user: dict = Depends(require_client)):
    # For demo: return all invoices; filter by customer_email if desired
    return {"invoices": INVOICES}

# Client profile
@app.put("/client/profile")
def update_client_profile(req: ClientProfileUpdate, user: dict = Depends(require_client)):
    for field, val in req.dict(exclude_unset=True).items():
        if val is not None:
            user[field] = val
    return {k: v for k, v in user.items() if k != "password"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
