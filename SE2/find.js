document.querySelector("a[href='#home']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "home.html"; // Change to your actual landing page URL
});

document.querySelector("a[href='#browse']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "browse.html"; // Change to your actual landing page URL
});