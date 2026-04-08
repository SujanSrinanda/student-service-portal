const API = "http://127.0.0.1:8000";

/* =========================
   CONTACT FORM
========================= */

async function submitContact() {

let name = document.getElementById("name").value.trim();
let email = document.getElementById("email").value.trim();
let message = document.getElementById("message").value.trim();

if (!name || !email || !message) {
alert("Please fill all fields");
return;
}

try {

let res = await fetch(API + "/submit-contact", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({ name, email, message })
});

if (res.ok) {

showSuccess("successMessage", "Request submitted successfully!");

document.getElementById("name").value = "";
document.getElementById("email").value = "";
document.getElementById("message").value = "";

} else {

alert("Something went wrong");

}

} catch (err) {

alert("Server connection failed");

}

}


/* =========================
   ADMIN TABLE
========================= */

async function loadContacts() {

try {

let res = await fetch(API + "/contacts");
let data = await res.json();

let table = document.getElementById("contactTable");

if (!table) return;

table.innerHTML = "";

data.forEach(c => {

table.innerHTML += `

<tr class="border-b hover:bg-gray-50">

<td class="p-3">${c.id}</td>
<td>${c.name}</td>
<td>${c.email}</td>
<td>${c.message}</td>

<td>
<button onclick="deleteContact(${c.id})"
class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition">

Delete

</button>
</td>

</tr>

`;

});

updateStats(data);

} catch (err) {

console.error("Failed to load contacts");

}

}


/* =========================
   DELETE CONTACT
========================= */

async function deleteContact(id) {

let confirmDelete = confirm("Delete this message?");

if (!confirmDelete) return;

await fetch(API + "/contacts/" + id, {
method: "DELETE"
});

loadContacts();

}


/* =========================
   LOGIN
========================= */

async function login() {

let username = document.getElementById("username").value.trim();
let password = document.getElementById("password").value.trim();

if (!username || !password) {
alert("Enter username and password");
return;
}

try {

let res = await fetch(API + "/login", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({ username, password })
});

if (res.status === 200) {

window.location.href = "/admin";

} else {

showError("loginError", "Invalid username or password");

}

} catch (err) {

alert("Server error");

}

}


/* =========================
   UI HELPERS
========================= */

function showSuccess(id, message) {

let box = document.getElementById(id);

if (!box) return;

box.innerText = message;

box.classList.remove("hidden");

setTimeout(() => {
box.classList.add("hidden");
}, 3000);

}


function showError(id, message) {

let box = document.getElementById(id);

if (!box) return;

box.innerText = message;

box.classList.remove("hidden");

}


function updateStats(data) {

let total = document.getElementById("totalMessages");

if (total) {
total.innerText = data.length;
}

}