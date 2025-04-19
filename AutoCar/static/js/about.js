document.addEventListener('DOMContentLoaded', function () {
    // Redirect to home page when HOME button is clicked
    const homeLink = document.querySelector("a[href='#home']");
    if (homeLink) {
        homeLink.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default anchor behavior
            window.location.href = "/"; // Django root URL
        });
    }

    // Redirect to about page when ABOUT US button is clicked
    const aboutLink = document.querySelector("a[href='#about']");
    if (aboutLink) {
        aboutLink.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default anchor behavior
            window.location.href = "/about/"; // Django about URL
        });
    }

    // Toggle FAQ answers
    const faqHeaders = document.querySelectorAll('.faq-item h3');
    faqHeaders.forEach((header, index) => {
        header.addEventListener('click', function () {
            toggleFAQ(index + 1);
        });
    });

    // Find all links in the navigation
    const links = document.querySelectorAll('a');

    // Loop through all links and hide those that contain LOGIN or SIGN UP
    links.forEach(function (link) {
        if (link.textContent === 'LOGIN' || link.textContent === 'SIGN UP') {
            link.style.display = 'none';
        }
    });
});

// Toggle FAQ answers function - keeps your original function
function toggleFAQ(index) {
    const faqItem = document.querySelectorAll('.faq-item')[index - 1];

    // Toggle active class
    faqItem.classList.toggle('active');

    // Get the paragraph and icon within this FAQ item
    const paragraph = faqItem.querySelector('p');
    const icon = faqItem.querySelector('i');

    // Toggle display and icon
    if (paragraph.style.display === 'block') {
        paragraph.style.display = 'none';
        if (icon) {
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }
    } else {
        paragraph.style.display = 'block';
        if (icon) {
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        }
    }
}