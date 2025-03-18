// Navigation handlers
document.addEventListener('DOMContentLoaded', function () {
    // Handle all navigation links in the header
    const navLinks = document.querySelectorAll("nav a");
    navLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            // If it's not an anchor link (doesn't start with #), let the default behavior work
            if (!this.getAttribute('href').startsWith('#')) {
                // This allows the link to work normally (no need to prevent default)
                // The href will be the proper Django-generated URL
            }
        });
    });

    // Initialize FAQ items to make sure they're properly set up
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        // Hide all FAQ paragraphs initially
        const paragraph = item.querySelector('p');
        if (paragraph) {
            paragraph.style.display = 'none';
        }

        // Make sure icons are set correctly
        const icon = item.querySelector('i');
        if (icon) {
            icon.className = 'fas fa-chevron-down';
        }
    });
});

function toggleFAQ(id) {
    // Get all FAQ items
    const faqItems = document.querySelectorAll('.faq-item');

    // Convert the NodeList to an Array for easier handling
    const faqItemsArray = Array.from(faqItems);

    // Subtract 1 from id since arrays are 0-indexed but our FAQ IDs start at 1
    const index = id - 1;

    // Find the selected item by its index in the array
    const selectedItem = faqItemsArray[index];

    if (!selectedItem) {
        console.error(`FAQ item #${id} not found`);
        return;
    }

    // Toggle the active class on the selected item
    selectedItem.classList.toggle('active');

    // Show/hide the paragraph
    const paragraph = selectedItem.querySelector('p');
    if (!paragraph) {
        console.error(`No paragraph found in FAQ item #${id}`);
        return;
    }

    // Toggle display
    if (paragraph.style.display === 'block') {
        paragraph.style.display = 'none';
        const icon = selectedItem.querySelector('i');
        if (icon) icon.className = 'fas fa-chevron-down';
    } else {
        paragraph.style.display = 'block';
        const icon = selectedItem.querySelector('i');
        if (icon) icon.className = 'fas fa-chevron-up';
    }

    // Close other FAQs
    faqItems.forEach((item, idx) => {
        if (idx !== index) {
            // Remove active class from other items
            item.classList.remove('active');

            const otherParagraph = item.querySelector('p');
            if (otherParagraph) otherParagraph.style.display = 'none';

            const otherIcon = item.querySelector('i');
            if (otherIcon) otherIcon.className = 'fas fa-chevron-down';
        }
    });
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 100, // Adjust for header height
                behavior: 'smooth'
            });
        }
    });
});