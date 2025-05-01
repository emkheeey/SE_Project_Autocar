// Filter functions
function showAllCars(button) {
    setActiveFilterButton(button);
    // Here you would normally filter the cars, but since we're using placeholders it's just UI changes
}

function showBodyTypeFilters(button) {
    setActiveFilterButton(button);
    // Show body type sub-filters if needed
}

function showPriceFilters(button) {
    setActiveFilterButton(button);
    // Show price sub-filters if needed
}

function showTransmissionFilters(button) {
    setActiveFilterButton(button);
    // Show transmission sub-filters if needed
}

// Helper to set the active filter button
function setActiveFilterButton(button) {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active');
}

// Search function
function searchCars() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    console.log("Searching for:", searchTerm);
    // In the future, this would filter the cars based on the search term
}

// Toggle profile menu
document.addEventListener('DOMContentLoaded', function () {
    // Handle profile icon click
    const profileIcon = document.querySelector('.profile-icon');
    const userMenu = document.querySelector('.user-menu');

    if (profileIcon && userMenu) {
        // Hide user menu initially
        userMenu.style.display = 'none';

        // Toggle when profile icon is clicked
        profileIcon.addEventListener('click', function (e) {
            e.stopPropagation();
            if (userMenu.style.display === 'none' || !userMenu.style.display) {
                userMenu.style.display = 'block';
            } else {
                userMenu.style.display = 'none';
            }
        });

        // Close menu when clicking elsewhere on the page
        document.addEventListener('click', function (e) {
            if (userMenu.style.display === 'block' && !userMenu.contains(e.target)) {
                userMenu.style.display = 'none';
            }
        });
    }
});