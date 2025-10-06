let submitBtn = document.getElementById("submitBtn");
let alertDiv = document.getElementById("alert");

submitBtn.addEventListener("click", async () => {
    let username = document.getElementById("username").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let confirm_password = document.getElementById("confirm_password").value;

    // validate data 
    if (username === null || username === "") {
        alertDiv.hidden = false
        alertDiv.textContent = "Username not provided"
        return;
    }
    if (email === null || email === "") {
        alertDiv.hidden = false
        alertDiv.textContent = "Email not provided"
        return;
    }
    if (password === null || password === "") {
        alertDiv.hidden = false
        alertDiv.textContent = "Password not provided"
        return;
    }
    if (confirm_password === null || confirm_password === "") {
        alertDiv.hidden = false
        alertDiv.textContent = "Confrim password not provided"
        return;
    }
    if (confirm_password !== password){
        alertDiv.hidden = false
        alertDiv.textContent = "Confrim password not provided"
        alertDiv.classList.remove("alert-warning")
        alertDiv.classList.add("alert-danger")
        return;
    }

    var token = localStorage.getItem("access_token")
    fetch("http://127.0.0.1:8000/users", {
        "method": "POST",
        headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        body: JSON.stringify({
            "email": email,
            "username": username,
            "password": password,
            "confirm_password": confirm_password
        })
    })
    .then((response) => {
        let data = response.json();
        if (response.status !== 200) {
            alertDiv.hidden = false
            alertDiv.textContent = data.message
            alertDiv.classList.remove("alert-warning")
            alertDiv.classList.add("alert-danger")
            return;
        } else {
            window.location.href = "view.html"
        }
    })
    .catch((error) => {
        console.log(error)
        alertDiv.hidden = false
        alertDiv.textContent = "Unable to create user"
        alertDiv.classList.remove("alert-warning")
        alertDiv.classList.add("alert-danger")
        return;
    })
    
})