const API="http://127.0.0.1:8000"

async function submitContact(){

const name=document.getElementById("name").value
const email=document.getElementById("email").value
const message=document.getElementById("message").value

if(!name || !email || !message){
alert("All fields required")
return
}

const res=await fetch(API+"/submit-contact",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
name:name,
email:email,
message:message
})
})

const data=await res.json()

alert(data.message)

document.getElementById("name").value=""
document.getElementById("email").value=""
document.getElementById("message").value=""
}

async function loadContacts(){

const res=await fetch(API+"/contacts")

const contacts=await res.json()

const table=document.getElementById("contactTable")

table.innerHTML=""

contacts.forEach(c=>{

const row=document.createElement("tr")

row.innerHTML=`
<td>${c.id}</td>
<td>${c.name}</td>
<td>${c.email}</td>
<td>${c.message}</td>
<td>
<button onclick="deleteContact(${c.id})">Delete</button>
</td>
`

table.appendChild(row)

})

}

async function deleteContact(id){

await fetch(API+"/contacts/"+id,{
method:"DELETE"
})

loadContacts()

}

async function login(){

const username=document.getElementById("username").value
const password=document.getElementById("password").value

const res=await fetch(API+"/login",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
username:username,
password:password
})
})

if(res.status===200){

window.location.href="admin.html"

}else{

alert("Invalid credentials")

}

}