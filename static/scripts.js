document.addEventListener("DOMContentLoaded", function () {
    // Validate Login Form
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            if (email.trim() === "" || password.trim() === "") {
                alert("All fields are required!");
                event.preventDefault();
            }
        });
    }

    // Validate Register Form
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            const username = document.getElementById("username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            if (username.trim() === "" || email.trim() === "" || password.trim() === "") {
                alert("All fields are required!");
                event.preventDefault();
            }
        });
    }
});
