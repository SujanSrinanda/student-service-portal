from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Student Service Portal")

# -----------------------------
# Enable CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "frontend")
)

DB_FILE = os.path.join(BASE_DIR, "contacts.json")

# -----------------------------
# Serve Static Files (CSS + JS)
# -----------------------------

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# -----------------------------
# Models
# -----------------------------

class Contact(BaseModel):
    name: str
    email: str
    message: str


class Login(BaseModel):
    username: str
    password: str


# -----------------------------
# Database Helpers
# -----------------------------

def read_contacts():
    with open(DB_FILE, "r") as f:
        return json.load(f)


def write_contacts(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


if not os.path.exists(DB_FILE):
    write_contacts([])

# -----------------------------
# Frontend Pages
# -----------------------------

@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "home.html"))


@app.get("/about")
def about():
    return FileResponse(os.path.join(FRONTEND_DIR, "about.html"))


@app.get("/services")
def services():
    return FileResponse(os.path.join(FRONTEND_DIR, "services.html"))


@app.get("/contact")
def contact():
    return FileResponse(os.path.join(FRONTEND_DIR, "contact.html"))


@app.get("/login")
def login_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))


@app.get("/admin")
def admin_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))

# -----------------------------
# API: Submit Contact
# -----------------------------

@app.post("/submit-contact")
def submit_contact(contact: Contact):

    contacts = read_contacts()

    new_contact = {
        "id": len(contacts) + 1,
        "name": contact.name,
        "email": contact.email,
        "message": contact.message
    }

    contacts.append(new_contact)

    write_contacts(contacts)

    return {"message": "Contact submitted successfully"}

# -----------------------------
# API: Get All Contacts
# -----------------------------

@app.get("/contacts")
def get_contacts():
    return read_contacts()

# -----------------------------
# API: Get Contact by ID
# -----------------------------

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):

    contacts = read_contacts()

    for contact in contacts:
        if contact["id"] == contact_id:
            return contact

    raise HTTPException(status_code=404, detail="Contact not found")

# -----------------------------
# API: Update Contact
# -----------------------------

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, updated_contact: Contact):

    contacts = read_contacts()

    for contact in contacts:
        if contact["id"] == contact_id:

            contact["name"] = updated_contact.name
            contact["email"] = updated_contact.email
            contact["message"] = updated_contact.message

            write_contacts(contacts)

            return {"message": "Contact updated successfully"}

    raise HTTPException(status_code=404, detail="Contact not found")

# -----------------------------
# API: Delete Contact
# -----------------------------

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):

    contacts = read_contacts()

    for contact in contacts:
        if contact["id"] == contact_id:

            contacts.remove(contact)

            write_contacts(contacts)

            return {"message": "Contact deleted successfully"}

    raise HTTPException(status_code=404, detail="Contact not found")

# -----------------------------
# API: Admin Login
# -----------------------------

@app.post("/login")
def login(credentials: Login):

    ADMIN_USER = "SUJAN"
    ADMIN_PASS = "123456"

    if credentials.username == "SUJAN" and credentials.password == "123456":
        return {"message": "Login successful"}

    raise HTTPException(status_code=401, detail="Invalid credentials")