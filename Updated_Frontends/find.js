document.querySelector("a[href='#home']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "home.html"; // Change to your actual landing page URL
});

document.querySelector("a[href='#browse']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "browse.html"; // Change to your actual landing page URL
});

document.querySelector("a[href='#compare']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "compare.html"; // Change to your actual landing page URL
});

document.getElementById("toggleQuestion").addEventListener("click", function () {
    let checkboxContainer = document.getElementById("checkboxContainer");
    checkboxContainer.classList.toggle("hidden");
});

function toggleMenu() {
    var menu = document.getElementById("userMenu");
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}

// Logout function
function logout() {
    // Clear local storage (if used for storing user data)
    localStorage.removeItem("currentUser");
    
    // Redirect to login page
    alert("Logging out...");
    window.location.href = "login.html";
}

// Close the menu if clicked outside
window.onclick = function(event) {
    var menu = document.getElementById("userMenu");
    var icon = document.querySelector(".profile-icon");
    if (event.target !== icon && !icon.contains(event.target) && event.target !== menu && !menu.contains(event.target)) {
        menu.style.display = "none";
    }
}