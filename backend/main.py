from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Student Service Portal API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "contacts.json"

# ----------------------------
# Models
# ----------------------------

class Contact(BaseModel):
    name: str
    email: str
    message: str


class Login(BaseModel):
    username: str
    password: str


# ----------------------------
# Utility Functions
# ----------------------------

def read_contacts():
    with open(DB_FILE, "r") as f:
        return json.load(f)


def write_contacts(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Create DB file if not exists
if not os.path.exists(DB_FILE):
    write_contacts([])


# ----------------------------
# Root API
# ----------------------------

@app.get("/")
def root():
    return {"message": "Student Service Portal API Running"}


# ----------------------------
# Submit Contact
# ----------------------------

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

    return {"message": "Contact submitted successfully", "data": new_contact}


# ----------------------------
# Get All Contacts
# ----------------------------

@app.get("/contacts")
def get_contacts():
    return read_contacts()


# ----------------------------
# Get Contact by ID
# ----------------------------

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):

    contacts = read_contacts()

    for contact in contacts:
        if contact["id"] == contact_id:
            return contact

    raise HTTPException(status_code=404, detail="Contact not found")


# ----------------------------
# Update Contact
# ----------------------------

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, updated_contact: Contact):

    contacts = read_contacts()

    for contact in contacts:

        if contact["id"] == contact_id:

            contact["name"] = updated_contact.name
            contact["email"] = updated_contact.email
            contact["message"] = updated_contact.message

            write_contacts(contacts)

            return {"message": "Contact updated successfully", "data": contact}

    raise HTTPException(status_code=404, detail="Contact not found")


# ----------------------------
# Delete Contact
# ----------------------------

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):

    contacts = read_contacts()

    for contact in contacts:

        if contact["id"] == contact_id:

            contacts.remove(contact)

            write_contacts(contacts)

            return {"message": "Contact deleted successfully"}

    raise HTTPException(status_code=404, detail="Contact not found")


# ----------------------------
# Admin Login
# ----------------------------

@app.post("/login")
def login(credentials: Login):

    ADMIN_USER = "admin"
    ADMIN_PASS = "admin123"

    if credentials.username == "SUJAN" and credentials.password == "123456":
        return {"message": "Login successful"}

    raise HTTPException(status_code=401, detail="Invalid credentials")