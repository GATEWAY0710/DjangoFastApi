var submitBtn = document.getElementById("submitBtn");

submitBtn.addEventListener("click", async (event) => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const request = new Request("http://127.0.0.1:8000/auth/token", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const response = await fetch(request);
        const data = await response.json();

        if (response.status !== 200) {
            window.alert(data.message || "Invalid login credentials");
        } else {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);
            localStorage.setItem("expires_in", data.expires_in);
            window.location.href = "view.html";
        }
    } catch (error) {
        console.error("Error:", error);
        window.alert("An error occurred while processing your request.");
    }
});

