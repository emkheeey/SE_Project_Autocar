document.querySelector("a[href='#home']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "home.html"; // Change to your actual landing page URL
});

document.querySelector("a[href='#recommend']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "find.html"; // Change to your actual landing page URL
});