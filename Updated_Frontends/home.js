document.querySelector(".browsebtn").addEventListener("click", function() {
    window.location.href = "browse.html"; // Change this to your actual car listing page
});

document.querySelector(".comparebtn").addEventListener("click", function() {
    window.location.href = "compare.html"; // Change this to your actual recommendation system page
});

document.querySelector("a[href='#compare-cars']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "compare.html"; // Change to your actual landing page URL
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