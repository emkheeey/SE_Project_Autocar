       function login() {
            const username = document.getElementById("login-username").value;
            const password = document.getElementById("login-password").value;

            if (username && password) {
                setTimeout(() => {
                    window.location.href = 'home.html';
                }, 500);
            } else {
                alert("Please enter both username and password.");
            }
        }

        function signup() {
            const firstname = document.getElementById("signup-firstname").value;
            const lastname = document.getElementById("signup-lastname").value;
            const email = document.getElementById("signup-email").value;
            const password = document.getElementById("signup-password").value;
            const confirmpass = document.getElementById("confirm-password").value;

            if (firstname && lastname && email && password && confirmpass) {
                alert("Signup successful! You can now log in.");
                toggleForm();
            } else {
                alert("Please fill in all fields.");
            }
        }

        function toggleForm() {
            const loginContainer = document.getElementById("login-container");
            const signupContainer = document.getElementById("signup-container");

            if (loginContainer.style.display === "none") {
                loginContainer.style.display = "block";
                signupContainer.style.display = "none";
            } else {
                loginContainer.style.display = "none";
                signupContainer.style.display = "block";
            }
        }

// Redirect to landing page when HOME button is clicked
document.querySelector("a[href='#home']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "landingpage.html"; // Change to your actual landing page URL
});

// Redirect to landing page when ABOUT US button is clicked
document.querySelector("a[href='#about']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "about.html"; // Change to your actual landing page URL
});