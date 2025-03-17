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

// Toggle FAQ answers
function toggleFAQ(index) {
    const faqItem = document.querySelectorAll('.faq-item')[index - 1];
    faqItem.classList.toggle('active');
}





